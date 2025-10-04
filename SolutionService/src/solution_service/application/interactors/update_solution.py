from dataclasses import dataclass

from solution_service.application.dto import SolutionCheckResult
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)


@dataclass(frozen=True, slots=True)
class StoreCheckedSolution:
    solution_repository: SolutionRepository

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
