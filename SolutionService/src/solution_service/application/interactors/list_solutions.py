from collections.abc import Collection, Sequence
from dataclasses import dataclass

from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.domain.abstract import AnySolution, TaskType


@dataclass(frozen=True, slots=True)
class ListMySolutions:
    """Get all my solutions."""

    solutions: SolutionRepository
    user_idp: UserIdProvider

    async def __call__(self) -> Collection[AnySolution]:
        user = await self.user_idp.require_user()
        return await self.solutions.get_all_solutions_of_user(user.id)


@dataclass(frozen=True, slots=True)
class ListMySolutionsOnTask:
    """Get all my solutions for specific task."""

    solutions: SolutionRepository
    user_idp: UserIdProvider

    async def __call__(
        self,
        task_type: TaskType,
        task_id: int,
    ) -> Sequence[AnySolution]:
        user = await self.user_idp.require_user()
        return await self.solutions.get_all_solutions_of_task(
            user.id,
            task_type,
            task_id,
        )
