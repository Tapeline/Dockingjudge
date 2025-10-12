from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from solution_service.domain.abstract import AnySolution, TaskType


@dataclass
class UserContestStatus:
    """How well is user doing in the contest."""

    tasks_attempted: int
    tasks_solved: int
    solutions: list[AnySolution | None]
    total_score: int


@dataclass
class UserSolutionScore:
    """A reduced class of solution."""

    task_id: int
    task_type: TaskType
    user_id: int
    score: int
    short_verdict: str


@dataclass
class UserStandingRow:
    """How well is user doing in the contest."""

    tasks_attempted: int
    tasks_solved: int
    solutions: list[UserSolutionScore | None]
    total_score: int


@dataclass
class PaginationParameters:
    """Limit-offset pagination."""

    offset: int = 0
    limit: int | None = None


class SolutionRepository(Protocol):
    """Abstraction layer for solution storage."""

    @abstractmethod
    async def get_all_solutions_of_user(
        self,
        user_id: int,
        task_type: TaskType | None = None,
        pagination_params: PaginationParameters | None = None,
    ) -> list[AnySolution]:
        """Get all authored solutions."""
        raise NotImplementedError

    @abstractmethod
    async def get_all_solutions_of_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
        pagination_params: PaginationParameters | None = None,
    ) -> list[AnySolution]:
        """Get all task solutions."""
        raise NotImplementedError

    @abstractmethod
    async def get_all_solutions_of_user_for_contest(
        self,
        user_id: int,
        contest_tasks: Sequence[tuple[TaskType, int]],
        pagination_params: PaginationParameters | None = None,
    ) -> Sequence[AnySolution]:
        """Get all solutions of a user for a contest."""
        raise NotImplementedError

    @abstractmethod
    async def get_contest_standings(
        self,
        contest_tasks: Sequence[tuple[TaskType, int]],
        participants: Sequence[int],
    ) -> dict[int, UserStandingRow]:
        """Get contest standings."""
        raise NotImplementedError

    @abstractmethod
    async def get_solution(
        self,
        solution_id: str,
    ) -> AnySolution | None:
        """Get a solution by its id."""
        raise NotImplementedError

    @abstractmethod
    async def get_best_solution_by_user_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
    ) -> AnySolution | None:
        """Get the best solution for a user on a task."""
        raise NotImplementedError

    @abstractmethod
    async def create_solution(
        self,
        solution: AnySolution,
    ) -> None:
        """Create a new solution."""
        raise NotImplementedError

    @abstractmethod
    async def store_solution_check_result(
        self,
        solution_id: str,
        score: int,
        detailed_verdict: str,
        short_verdict: str,
        group_scores: dict[str, int],
        protocol: dict[str, Any],
    ) -> None:
        """Store the result of a solution check."""
        raise NotImplementedError

    @abstractmethod
    async def purge_user_solutions(self, user_id: int) -> None:
        """Purge all solutions of a user."""
        raise NotImplementedError

    @abstractmethod
    async def purge_task_solutions(
        self, task_type: TaskType, task_id: int,
    ) -> None:
        """Purge all solutions for a task."""
        raise NotImplementedError
