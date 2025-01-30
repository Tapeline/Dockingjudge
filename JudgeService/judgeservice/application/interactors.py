from dishka import FromDishka

from judgeservice.application.interfaces import JudgeletPool, SolutionGateway
from judgeservice.domain.entities import Solution, JudgeletAnswer, TestCaseResult


class ProcessSolutionInteractor:
    def __init__(
            self,
            judgelet_pool: FromDishka[JudgeletPool],
            solution_gateway: FromDishka[SolutionGateway]
    ):
        self.judgelet_pool = judgelet_pool
        self.solution_gateway = solution_gateway

    async def __call__(self, solution: Solution) -> None:
        judgelet = await self.judgelet_pool.get_for_compiler(
            solution.compiler
        )
        solution.solution_data = await self.solution_gateway.get_solution_file(
            solution.solution_url
        )
        judgelet_response = await judgelet.check_solution(solution)
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


def _get_first_failed(group_protocol: list[TestCaseResult]) -> str:
    for test_no, test in enumerate(group_protocol):
        if test.is_successful:
            continue
        return f"Test #{test_no}: {test.verdict}"
    return "OK"
