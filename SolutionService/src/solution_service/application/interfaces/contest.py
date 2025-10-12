from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, NamedTuple, Protocol

from pydantic import BaseModel, Field

from solution_service.domain.abstract import TaskType


class ValidatorDTO(BaseModel):
    """Resembles a single answer validator."""

    type: str
    args: dict[str, Any]


class QuizTaskDTO(BaseModel):
    """Resembles a single quiz task."""

    contest_id: int = Field(alias="contest")
    id: int
    title: str
    description: str
    validator: ValidatorDTO
    points: int


class CodeTaskDTO(BaseModel):
    """Resembles a single code task."""

    contest_id: int = Field(alias="contest")
    id: int
    title: str
    description: str
    test_suite: dict[str, Any]


type AnyTaskDTO = QuizTaskDTO | CodeTaskDTO


class ContestTaskHead(NamedTuple):
    """A shorter version of contest task info."""

    type: TaskType
    id: int
    title: str


class ContestService(Protocol):
    """Provides methods to work with contests."""

    @abstractmethod
    async def get_contest_managers(self, contest_id: int) -> Sequence[int]:
        """Get users that can manage the contest."""
        raise NotImplementedError

    @abstractmethod
    async def get_contest_tasks(
        self, contest_id: int,
    ) -> Sequence[ContestTaskHead]:
        """Get tasks of contest (header info only)."""
        raise NotImplementedError

    @abstractmethod
    async def get_contest_participants(
        self, contest_id: int,
    ) -> Sequence[int]:
        """Get list of users who participate in this contest."""
        raise NotImplementedError

    @abstractmethod
    async def can_submit(
        self, user_id: int, task_type: TaskType, task_id: int,
    ) -> bool:
        """Ask contest service a permission to submit this task."""
        raise NotImplementedError

    @abstractmethod
    async def get_task(
        self, task_type: str, task_id: int,
    ) -> AnyTaskDTO | None:
        """Get full task definition."""
        raise NotImplementedError

    @abstractmethod
    async def get_quiz_task(self, task_id: int) -> QuizTaskDTO | None:
        """Get full quiz task definition."""
        raise NotImplementedError

    @abstractmethod
    async def get_code_task(self, task_id: int) -> CodeTaskDTO | None:
        """Get full code task definition."""
        raise NotImplementedError
