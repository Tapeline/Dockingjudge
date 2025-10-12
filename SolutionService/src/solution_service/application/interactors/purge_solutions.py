from dataclasses import dataclass

from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.storage import DBSession
from solution_service.domain.abstract import TaskType


@dataclass(frozen=True, slots=True)
class PurgeUserSolutions:
    """Purges all solutions of a user."""
    solution_repository: SolutionRepository
    session: DBSession

    async def __call__(self, user_id: int) -> None:
        await self.solution_repository.purge_user_solutions(user_id)
        await self.session.commit()


@dataclass(frozen=True, slots=True)
class PurgeTaskSolutions:
    """Purges all solutions for a task."""
    solution_repository: SolutionRepository
    session: DBSession

    async def __call__(self, task_type: TaskType, task_id: int) -> None:
        await self.solution_repository.purge_task_solutions(
            task_type, task_id,
        )
        await self.session.commit()
