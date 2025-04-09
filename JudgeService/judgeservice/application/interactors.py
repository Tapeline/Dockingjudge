import logging

from dishka import FromDishka

from judgeservice.application.interfaces import JudgeletPool, SolutionGateway
from judgeservice.domain.entities import (
    GroupProtocolSchema,
    Solution,
    JudgeletAnswer,
)


class ProcessSolutionInteractor:
    def __init__(
            self,
            judgelet_pool: FromDishka[JudgeletPool],
            solution_gateway: FromDishka[SolutionGateway]
    ):
        self.judgelet_pool = judgelet_pool
        self.solution_gateway = solution_gateway

    async def __call__(self, solution: Solution) -> None:
        logging.info("Retrieving target judgelet")
        judgelet = await self.judgelet_pool.get_for_compiler(
            solution.compiler
        )
        logging.info("Retrieving solution file")
        solution.solution_data = await self.solution_gateway.get_solution_file(
            solution.solution_url
        )
        logging.info("Communicating with judgelet")
        judgelet_response = await judgelet.check_solution(solution)
        logging.info("Checking successful")
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
    verdict = "Some tests failed:\n"
    for group_name, group_protocol in judgelet_response.protocol.items():
        verdict += "Group {0}: {1}\n".format(
            group_name,
            _get_first_failed(group_protocol)
        )
    return verdict


def _get_first_failed(group_protocol: GroupProtocolSchema) -> str:
    for test_no, verdict in enumerate(group_protocol.verdicts):
        if verdict.is_successful:
            continue
        return f"Test #{test_no}: {verdict.codename}"
    return "OK"
