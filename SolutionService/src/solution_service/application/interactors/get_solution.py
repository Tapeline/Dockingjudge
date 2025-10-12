from dataclasses import dataclass

from solution_service.application.exceptions import MayNotAccessSolution
from solution_service.application.interfaces.contest import ContestService
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.domain.abstract import AnySolution, TaskType


@dataclass(frozen=True, slots=True)
class GetBestSolutionForUserOnTask:
    """Gets the best solution for a user on a specific task."""

    solution_repository: SolutionRepository
    user_idp: UserIdProvider

    async def __call__(
        self,
        task_type: str,
        task_id: int,
    ) -> AnySolution | None:
        """Gets the best solution for a user on a specific task."""
        user = await self.user_idp.require_user()
        return await self.solution_repository.get_best_solution_by_user_task(
            user.id,
            TaskType(task_type),
            task_id,
        )


@dataclass(frozen=True, slots=True)
class GetSolution:
    """Gets a solution by its id."""

    solution_repository: SolutionRepository
    contest_service: ContestService
    user_idp: UserIdProvider

    async def __call__(
        self,
        solution_id: str,
    ) -> AnySolution | None:
        """Gets a solution by its id."""
        solution = await self.solution_repository.get_solution(solution_id)
        if not solution:
            return None
        contest_managers = await self.contest_service.get_contest_managers(
            solution.contest_id,
        )
        user = await self.user_idp.require_user()
        if user.id != solution.user_id and user.id not in contest_managers:
            raise MayNotAccessSolution
        return solution
