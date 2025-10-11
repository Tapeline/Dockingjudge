from dataclasses import dataclass

import structlog

from judgeservice.application.interfaces import JudgeletPool, SolutionGateway
from judgeservice.domain.entities import (
    GroupProtocolSchema,
    JudgeletAnswer,
    Solution,
)

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class ProcessSolutionInteractor:
    """Select judgelet and proxy request."""

    judgelet_pool: JudgeletPool
    solution_gateway: SolutionGateway

    async def __call__(self, solution: Solution) -> None:
        """Get judgelet and proxy request."""
        logger.info("Retrieving target judgelet")
        judgelet = await self.judgelet_pool.get_for_compiler(
            solution.compiler,
        )
        logger.info("Retrieving solution file")
        solution.solution_data = await self.solution_gateway.get_solution_file(
            solution.solution_url,
        )
        logger.info("Communicating with judgelet")
        judgelet_response = await judgelet.check_solution(solution)
        logger.info("Checking successful")
        solution.score = judgelet_response.score
        solution.group_scores = judgelet_response.group_scores
        solution.short_verdict = judgelet_response.verdict
        solution.detailed_verdict = _form_detailed_verdict(judgelet_response)
        solution.protocol = judgelet_response.protocol


def _form_detailed_verdict(judgelet_response: JudgeletAnswer) -> str:
    if judgelet_response.verdict == "OK":
        return "All tests passed."
    if judgelet_response.compilation_error:
        return f"Compilation error:\n{judgelet_response.compilation_error}"
    verdict_lines = [
        f"Group {group_name}: {_get_first_failed(group_protocol)}"
        for group_name, group_protocol in judgelet_response.protocol.items()
    ]
    verdict_lines.insert(0, "Some tests failed:")
    return "\n".join(verdict_lines)


def _get_first_failed(group_protocol: GroupProtocolSchema) -> str:
    for test_no, verdict in enumerate(group_protocol.verdicts):
        if verdict.is_successful:
            continue
        return f"Test #{test_no}: {verdict.codename}"
    return "OK"
