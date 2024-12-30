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

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Sequence, TypeAlias, cast

import aiofiles
from parlant.adapters.db.json_file import JSONFileDocumentDatabase
from parlant.adapters.db.transient import TransientDocumentDatabase
from parlant.adapters.nlp.openai import OpenAIService
from parlant.core.common import DefaultBaseModel, Version, generate_id
from parlant.core.contextual_correlator import ContextualCorrelator
from parlant.core.logging import FileLogger, Logger, LogLevel, StdoutLogger
from parlant.core.nlp.generation import GenerationInfo
from parlant.core.nlp.service import NLPService
from parlant.core.persistence.common import ObjectId
from parlant.core.persistence.document_database import BaseDocument, DocumentDatabase
from typing_extensions import Self


@dataclass(frozen=True)
class Question:
    id: str
    variants: list[str]
    answer: str


async def parse_md_file(file: Path) -> Question:
    async with aiofiles.open(file) as f:
        variants: list[str] = []

        lines = await f.readlines()

        content_start = 0

        for line in lines:
            if not line.strip():
                content_start += 1
                continue
            if not line.startswith("# "):
                break

            variants.append(line[1:].strip())
            content_start += 1

        content_lines = lines[content_start:]
        content = "".join(content_lines).strip()

    return Question(
        id="",
        variants=variants,
        answer=content,
    )


AnswerGrade: TypeAlias = Literal["partial", "full", "no-answer"]


class _QuestionDocument(BaseDocument):
    variants: list[str]
    answer: str


class _RelevantQuotes(DefaultBaseModel):
    question_id: str
    quotes: list[str]


class _AnswerSchema(DefaultBaseModel):
    user_questions: list[str]
    relevant_question_variants: list[str] | None = None
    full_answer_can_be_found_in_background_info: bool
    partial_answer_can_be_found_in_background_info: bool
    insights_on_what_could_be_a_legitimate_answer: str | None = None
    collected_relevant_quotes_from_background_info: list[_RelevantQuotes] | None = None
    concise_and_minimal_synthesized_answer_based_solely_on_relevant_quotes: (
        str | None
    ) = None
    question_answered_in_full: bool
    question_answered_partially: bool
    question_not_answered_at_all: bool


@dataclass(frozen=True)
class Reference:
    question_id: str
    quotes: list[str]


@dataclass(frozen=True)
class Answer:
    content: str | None
    grade: AnswerGrade
    generation_info: GenerationInfo
    evaluation: str
    references: list[Reference]


class App:
    VERSION = Version.String("0.1.0")

    def __init__(
        self,
        database: DocumentDatabase,
        service: NLPService,
        logger: Logger,
    ):
        self._db = database
        self._service = service
        self.logger = logger

        self._questions: dict[str, Question] = {}

    async def __aenter__(self, *args: Any, **kwargs: Any) -> Self:
        self._collection = await self._db.get_or_create_collection(
            "questions",
            schema=_QuestionDocument,
        )

        self._generator = await self._service.get_schematic_generator(_AnswerSchema)

        persisted_questions = await self._collection.find({})

        for q in persisted_questions:
            assert "id" in q

            self._questions[q["id"]] = Question(
                id=q["id"],
                variants=q["variants"],
                answer=q["answer"],
            )

        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> bool:
        return False

    async def ask_question(self, question: str) -> Answer:
        self.logger.info(
            f'Looking for answer for "{question}" in {len(self._questions)} stored question(s)'
        )
        background_info = self._format_background_info()

        prompt = f"""\
You are a RAG agent who has exactly one job: to answer the user's question
based ONLY on the background information provided here in-context.

Note that there are cases when data is provided in the answer in a way that's
implied by the question for that answer. For example, if the question is
"What is Blabooshka" and the answer provided is "It's a banana", then
you can infer that "A Blabooshka is a banana".
In this way, the question variants themselves are directly connected to
their answers. Also, often, the answer is to be considered an explicit and
direct continuation of one of the question variants, as if continuing the idea or sentence.
This is only true within a particular question, its variants, and its answer.
It does not apply cross-questions (i.e. the answer to one question is never
a direct continuation of a different question).

Background Information: ###
{background_info}
###

User Question: ###
{question}
###

Produce a JSON object according to the following schema: ###
{{
    "user_questions": [ QUERY_1, ..., QUERY_N ],
    "relevant_question_variants": [ VARIANT_1, ..., VARIANT_N ],
    "full_answer_can_be_found_in_background_info": <BOOL>,
    "partial_answer_can_be_found_in_background_info": <BOOL>,
    "insights_on_what_could_be_a_legitimate_answer": <"YOUR INSIGHTS AS TO WHAT COULD BE A legitimate ANSWER">,
    "collected_relevant_quotes_from_background_info": [
        {{
            "question_id": QUESTION_ID,
            "quotes": [ QUOTE_1, ..., QUOTE_N ]
        }},
        ...
    ],
    "concise_and_minimal_synthesized_answer_based_solely_on_relevant_quotes": <"PRODUCE AN ANSWER HERE EXCLUSIVELY AND ONLY BASED ON THE COLLECTED QUOTES, WITHOUT ADDING ANYTHING ELSE">
    "question_answered_in_full": <BOOL>,
    "question_answered_partially": <BOOL>,
    "question_not_answered_at_all": <BOOL>
}}
###
"""

        result = await self._generator.generate(prompt)

        self.logger.debug(result.content.model_dump_json(indent=2))

        if (
            (
                not result.content.full_answer_can_be_found_in_background_info
                and not result.content.partial_answer_can_be_found_in_background_info
            )
            or not (
                result.content.question_answered_in_full
                or result.content.question_answered_partially
            )
            or result.content.question_not_answered_at_all
            or not result.content.collected_relevant_quotes_from_background_info
        ):
            self.logger.info("No answer")

            return Answer(
                content=None,
                evaluation=result.content.insights_on_what_could_be_a_legitimate_answer
                or "",
                grade="no-answer",
                generation_info=result.info,
                references=[],
            )

        answer = Answer(
            content=result.content.concise_and_minimal_synthesized_answer_based_solely_on_relevant_quotes,
            evaluation=result.content.insights_on_what_could_be_a_legitimate_answer
            or "",
            grade="full" if result.content.question_answered_in_full else "partial",
            generation_info=result.info,
            references=[
                Reference(
                    question_id=q.question_id,
                    quotes=q.quotes,
                )
                for q in result.content.collected_relevant_quotes_from_background_info
            ],
        )

        self.logger.info(
            f'Question: "{question}"; Answer ({answer.grade}): "{answer.content}"'
        )

        return answer

    def _format_background_info(self) -> str:
        if not self._questions:
            return "DATA NOT AVAILABLE"

        return "\n\n".join(
            [
                f"""\
Question #{q.id}[variants={q.variants}][[
Answer: {q.answer}
]]
"""
                for q in self._questions.values()
            ]
        )

    async def create_question(
        self,
        variants: list[str],
        answer: str,
    ) -> Question:
        new_id = generate_id()

        await self._collection.insert_one(
            _QuestionDocument(
                id=ObjectId(new_id),
                version=self.VERSION,
                variants=variants,
                answer=answer,
            )
        )

        question = Question(
            id=new_id,
            variants=variants,
            answer=answer,
        )

        self._questions[question.id] = question

        return question

    async def update_question(
        self,
        question_id: str,
        variants: list[str] | None = None,
        answer: str | None = None,
    ) -> Question:
        if question_id not in self._questions:
            raise KeyError()

        await self._collection.update_one(
            {"id": {"$eq": question_id}},
            params=cast(
                _QuestionDocument,
                {
                    **({"variants": variants} if variants else {}),
                    **({"answer": answer} if answer else {}),
                },
            ),
        )

        question = self._questions[question_id]

        self._questions[question_id] = Question(
            id=question.id,
            variants=variants or question.variants,
            answer=answer or question.answer,
        )

        return await self.read_question(question_id)

    async def read_question(self, question_id: str) -> Question:
        if question_id not in self._questions:
            raise KeyError()

        return self._questions[question_id]

    async def list_questions(self) -> Sequence[Question]:
        return list(self._questions.values())

    async def delete_question(self, question_id: str) -> bool:
        if question_id in self._questions:
            del self._questions[question_id]
            await self._collection.delete_one({"id": {"$eq": question_id}})
            return True
        return False


@asynccontextmanager
async def create_persistent_app(
    service: NLPService | None = None,
) -> AsyncIterator[App]:
    correlator = ContextualCorrelator()
    logger = FileLogger(
        Path("parlant-qna.log"),
        correlator,
        log_level=LogLevel.INFO,
        logger_id="parlant-qna",
    )

    if not service:
        service = OpenAIService(logger)

    async with JSONFileDocumentDatabase(
        logger=logger,
        file_path=Path("parlant-qna-db.json"),
    ) as db:
        with correlator.correlation_scope("parlant-qna"):
            async with App(db, service, logger) as app:
                logger.info("Initialized Parlant Q&A")
                yield app


@asynccontextmanager
async def create_transient_app() -> AsyncIterator[App]:
    correlator = ContextualCorrelator()
    logger = StdoutLogger(correlator, logger_id="parlant-qna")
    service = OpenAIService(logger)

    with correlator.correlation_scope("parlant-qna"):
        async with App(TransientDocumentDatabase(), service, logger) as app:
            yield app
