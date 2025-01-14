from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from solution_service.domain.entities.abstract import TaskType


@dataclass
class ValidatorDTO:
    type: str
    args: dict[str, Any]


@dataclass
class QuizTaskDTO:
    contest_id: int
    id: int
    title: str
    description: str
    validator: ValidatorDTO
    points: int


@dataclass
class CodeTaskDTO:
    contest_id: int
    id: int
    title: str
    description: str
    test_suite: dict


type AnyTaskDTO = QuizTaskDTO | CodeTaskDTO


class AbstractContestService(ABC):
    @abstractmethod
    async def get_contest_managers(self, contest_id: int) -> Sequence[int]:
        raise NotImplementedError

    @abstractmethod
    async def get_contest_tasks(self, contest_id: int) -> Sequence[tuple[TaskType, int]]:
        raise NotImplementedError

    @abstractmethod
    async def get_contest_participants(self, contest_id: int) -> Sequence[int]:
        raise NotImplementedError

    @abstractmethod
    async def can_submit(self, user_id: int, task_type: TaskType, task_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_task(self, task_type: str, task_id: int) -> AnyTaskDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_quiz_task(self, task_id: int) -> QuizTaskDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_code_task(self, task_id: int) -> CodeTaskDTO | None:
        raise NotImplementedError
