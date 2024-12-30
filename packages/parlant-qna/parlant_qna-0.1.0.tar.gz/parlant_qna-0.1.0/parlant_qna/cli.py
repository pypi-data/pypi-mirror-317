# Copyright 2024 Emcie Co Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
import sys
from dataclasses import dataclass
from typing import cast

import click
import httpx
import rich
from rich import box
from rich.table import Table

from parlant_qna.app import create_persistent_app
from parlant_qna.server import create_server

DEFAULT_PORT = 8807


async def run_server(port: int) -> None:
    async with (
        create_persistent_app() as qna_app,
        create_server(port, qna_app),
    ):
        pass


def main() -> None:
    @dataclass(frozen=True)
    class Config:
        server_address: str
        client: httpx.Client

    def get_client(ctx: click.Context) -> httpx.Client:
        return cast(Config, ctx.obj).client

    def die_if_error(response: httpx.Response, message: str | None = None) -> None:
        if response.is_success:
            return

        if message:
            rich.print(
                f"[red]error: {message}: http status code {response.status_code}"
            )
        else:
            rich.print(f"[red]error: http status code {response.status_code}")

        try:
            rich.print(response.json())
        except Exception:
            pass

        sys.exit(1)

    def success(message: str) -> None:
        rich.print(f"[green]{message}")

    @click.group("CLI")
    @click.option(
        "-s",
        "--server",
        type=str,
        help="QnA server address",
        metavar="ADDRESS[:PORT]",
        default=f"http://localhost:{DEFAULT_PORT}",
        show_default=True,
    )
    @click.pass_context
    def cli(ctx: click.Context, server: str) -> None:
        if not ctx.obj:
            ctx.obj = Config(
                server_address=server,
                client=httpx.Client(
                    base_url=server,
                    follow_redirects=True,
                    timeout=60,
                ),
            )

    @cli.command("server", help="Run as a standalone server")
    @click.option(
        "-p",
        "--port",
        metavar="PORT",
        help="Port number",
        default=DEFAULT_PORT,
        show_default=True,
    )
    def server(port: int) -> None:
        asyncio.run(run_server(port))

    @cli.command("ask", help="Ask a question")
    @click.argument("question", metavar="QUESTION")
    @click.pass_context
    def ask(ctx: click.Context, question: str) -> None:
        response = get_client(ctx).post("/answers", json={"query": question})

        die_if_error(response, "ask question")

        rich.print(response.json())

    @cli.command("add", help="Add a question/answer pair")
    @click.option(
        "-q",
        "--variant",
        help="Question variant (can be given multiple times for different ways to ask it)",
        multiple=True,
        required=True,
    )
    @click.option(
        "-a",
        "--answer",
        help="Answer text",
        required=True,
    )
    @click.pass_context
    def add(ctx: click.Context, variant: tuple[str], answer: str) -> None:
        response = get_client(ctx).post(
            "/questions",
            json={
                "variants": variant,
                "answer": answer,
            },
        )

        die_if_error(response, "add question")

        question_id = response.json()["question_id"]

        success(f"added question (id: {question_id})")

    @cli.command("update", help="Update a question")
    @click.argument("id", metavar="QUESTION_ID")
    @click.option(
        "-q",
        "--variant",
        help="New question variant (can be given multiple times for different ways to ask it). "
        "NOTE: Providing this will override any existing variants.",
        multiple=True,
    )
    @click.option(
        "-a",
        "--answer",
        help="New answer text",
    )
    @click.pass_context
    def update(
        ctx: click.Context,
        id: str,
        variant: tuple[str],
        answer: str | None,
    ) -> None:
        response = get_client(ctx).patch(
            f"/questions/{id}",
            json={
                **({"variants": variant} if variant else {}),
                **({"answer": answer} if answer else {}),
            },
        )

        die_if_error(response, "update question")

        question_id = response.json()["id"]

        success(f"updated question (id: {question_id})")

    @cli.command("list", help="List questions")
    @click.option(
        "-v",
        "--verbose",
        help="Show a lot of information about each answer",
        is_flag=True,
        default=False,
    )
    @click.pass_context
    def list_questions(ctx: click.Context, verbose: bool) -> None:
        response = get_client(ctx).get("/questions", params={"verbose": verbose})

        die_if_error(response, "list questions")

        questions = list(response.json())

        if not questions:
            rich.print("No data available")
            return

        table = Table(box=box.ROUNDED, border_style="bright_green")

        headers = questions[0].keys()

        for header in headers:
            table.add_column(header, header_style="bright_green", overflow="fold")

        for q in questions:
            table.add_row(*list(map(str, q.values())))

        rich.print(table)

    @cli.command("view", help="View a question")
    @click.argument("id", metavar="QUESTION_ID")
    @click.pass_context
    def view(ctx: click.Context, id: str) -> None:
        response = get_client(ctx).get(f"/questions/{id}")

        die_if_error(response, "view question")

        rich.print(response.json())

    @cli.command("remove", help="Remove a question")
    @click.argument("id", metavar="QUESTION_ID")
    @click.pass_context
    def remove(ctx: click.Context, id: str) -> None:
        response = get_client(ctx).delete(f"/questions/{id}")

        die_if_error(response, "delete question")

        success(f"deleted question (id: {id})")

    @cli.command(
        "help",
        context_settings={"ignore_unknown_options": True},
        help="Show help for a command",
    )
    @click.argument("command", nargs=-1, required=False)
    @click.pass_context
    def help_command(ctx: click.Context, command: tuple[str] | None = None) -> None:
        def transform_and_exec_help(command: str) -> None:
            new_args = [sys.argv[0]] + command.split() + ["--help"]
            os.execvp(sys.executable, [sys.executable] + new_args)

        if not command:
            click.echo(cli.get_help(ctx))
        else:
            transform_and_exec_help(" ".join(command))

    try:
        cli()
    except httpx.NetworkError as e:
        rich.print(f"[red]error: {e} ({type(e).__name__})")
        sys.exit(1)


if __name__ == "__main__":
    main()
