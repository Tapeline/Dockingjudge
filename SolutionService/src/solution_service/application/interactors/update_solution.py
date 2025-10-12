from dataclasses import dataclass

from solution_service.application.dto import SolutionCheckResult
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.storage import DBSession


@dataclass(frozen=True, slots=True)
class StoreCheckedSolution:
    """Stores the result of a solution check."""
    solution_repository: SolutionRepository
    session: DBSession

    async def __call__(
        self,
        solution_id: str,
        check_result: SolutionCheckResult,
    ) -> None:
        await self.solution_repository.store_solution_check_result(
            solution_id,
            check_result.score,
            check_result.detailed_verdict,
            check_result.short_verdict,
            check_result.group_scores,
            check_result.protocol,
        )
        await self.session.commit()
