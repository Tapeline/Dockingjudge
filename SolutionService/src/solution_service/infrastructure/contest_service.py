import logging
from typing import Sequence, override

import aiohttp
from dishka import FromDishka

from solution_service.application.interfaces import contest
from solution_service.application.interfaces.contest import (
    CodeTaskDTO,
    ContestTaskHead,
    QuizTaskDTO,
    AnyTaskDTO,
)
from solution_service.config import Config
from solution_service.domain.abstract import TaskType
from solution_service.infrastructure.exceptions import BadServiceResponseException


class ContestServiceImpl(contest.ContestService):
    def __init__(
        self,
        other_services: FromDishka[Config],
    ) -> None:
        self.base_url = other_services.services.contest_service
        self.internal_base_url = other_services.services.contest_service_internal
        self.logger = logging.getLogger("contest_service")

    @override
    async def get_contest_managers(self, contest_id: int) -> Sequence[int]:
        self.logger.info("Requesting contest managers for %s", contest_id)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.base_url}/contests/{contest_id}/managers/"
            ) as response,
        ):
            if response.status == 404:
                return []
            if response.status != 200:
                self.logger.error(
                    "/contests/%s/managers responded %s: %s",
                    contest_id, response.status, await response.text()
                )
                raise BadServiceResponseException("contest", response)
            return await response.json()

    @override
    async def get_contest_tasks(
        self, contest_id: int
    ) -> Sequence[ContestTaskHead]:
        self.logger.info("Requesting contest tasks for %s", contest_id)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.internal_base_url}/contests/{contest_id}/tasks/"
            ) as response,
        ):
            if response.status == 404:
                return []
            if response.status != 200:
                self.logger.error(
                    "/contests/%s/tasks responded %s: %s",
                    contest_id, response.status, await response.text()
                )
                raise BadServiceResponseException("contest", response)
            data = await response.json()
            return [
                ContestTaskHead(
                    TaskType(str(task["type"])),
                    int(task["id"]),
                    task["title"]
                )
                for task in data
            ]

    @override
    async def get_contest_participants(self, contest_id: int) -> Sequence[int]:
        self.logger.info("Requesting contest participants for %s", contest_id)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.base_url}/contests/{contest_id}/participants/"
            ) as response,
        ):
            if response.status == 404:
                return []
            if response.status != 200:
                self.logger.error(
                    "/contests/%s/participants responded %s: %s",
                    contest_id, response.status, await response.text()
                )
                raise BadServiceResponseException("contest", response)
            return await response.json()

    @override
    async def can_submit(
        self, user_id: int, task_type: TaskType, task_id: int
    ) -> bool:
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.base_url}/contests/tasks/"
                f"{task_type.value}/{task_id}/can-submit/{user_id}/"
            ) as response,
        ):
            if response.status != 200:
                return False
            return (await response.json())["can_submit"]

    @override
    async def get_task(
        self, task_type: str, task_id: int
    ) -> AnyTaskDTO | None:
        if task_type.lower() == "quiz":
            return await self.get_quiz_task(task_id)
        if task_type.lower() == "code":
            return await self.get_code_task(task_id)
        return None

    @override
    async def get_quiz_task(self, task_id: int) -> QuizTaskDTO | None:
        self.logger.info("Requesting task quiz:%s", task_id)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.internal_base_url}/contests/tasks/quiz/{task_id}/"
            ) as response,
        ):
            if response.status == 404:
                return None
            if response.status != 200:
                self.logger.error(
                    "internal/tasks/quiz/%s responded %s: %s",
                    task_id, response.status, await response.text()
                )
                raise BadServiceResponseException("contest", response)
            data = await response.json()
            return contest.QuizTaskDTO(**data)

    @override
    async def get_code_task(self, task_id: int) -> CodeTaskDTO | None:
        self.logger.info("Requesting task quiz:%s", task_id)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.internal_base_url}/contests/tasks/code/{task_id}/"
            ) as response,
        ):
            if response.status == 404:
                return None
            if response.status != 200:
                self.logger.error(
                    "internal/tasks/code/%s responded %s: %s",
                    task_id, response.status, await response.text()
                )
                raise BadServiceResponseException("contest", response)
            data = await response.json()
            return contest.CodeTaskDTO(**data)
