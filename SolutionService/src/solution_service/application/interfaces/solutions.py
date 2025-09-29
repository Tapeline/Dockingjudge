from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from solution_service.domain.entities.abstract import AnySolution, TaskType


@dataclass
class UserContestStatus:
    tasks_attempted: int
    tasks_solved: int
    solutions: list[AnySolution]
    total_score: int


@dataclass
class PaginationParameters:
    offset: int = 0
    limit: int | None = None


class AbstractSolutionRepository(ABC):
    """Abstraction layer for solution storage"""

    @abstractmethod
    async def get_all_solutions_of_user(
            self,
            user_id: int,
            task_type: TaskType | None,
            pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_solutions_of_task(
            self,
            user_id: int,
            task_type: TaskType,
            task_id: int,
            pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_solutions_of_user_for_contest(
            self,
            user_id: int,
            contest_tasks: Sequence[tuple[TaskType, int]],
            pagination_params: PaginationParameters | None = None
    ) -> Sequence[AnySolution]:
        raise NotImplementedError

    @abstractmethod
    async def get_contest_status_for_user(
            self,
            user_id: int,
            contest_tasks: Sequence[tuple[TaskType, int]]
    ) -> UserContestStatus:
        raise NotImplementedError

    @abstractmethod
    async def get_contest_standings(
            self,
            contest_tasks: Sequence[tuple[TaskType, int]],
            participants: Sequence[int],
    ) -> Sequence[UserContestStatus]:
        raise NotImplementedError

    @abstractmethod
    async def get_solution(
            self,
            solution_id: str
    ) -> AnySolution | None:
        raise NotImplementedError

    @abstractmethod
    async def get_best_solution_by_user_task(
            self,
            user_id: int,
            task_type: TaskType,
            task_id: int,
    ) -> AnySolution | None:
        raise NotImplementedError

    @abstractmethod
    async def create_solution(
            self,
            solution: AnySolution
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def store_solution_check_result(
            self,
            solution_id: str,
            score: int,
            detailed_verdict: str,
            short_verdict: str,
            group_scores: dict[str, int],
            protocol: dict,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def purge_user_solutions(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def purge_task_solutions(
            self, task_type: TaskType, task_id: int
    ) -> None:
        raise NotImplementedError
