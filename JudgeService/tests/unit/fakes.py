from judgeservice.application.interfaces import SolutionGateway
from judgeservice.domain.entities import (
    GroupProtocolSchema,
    Judgelet,
    JudgeletAnswer,
    Solution,
    VerdictSchema,
)


class FakeJudgelet(Judgelet):
    """Fake judgelet used for testing."""

    def __init__(
        self,
        address: str,
        *,
        is_alive: bool = True,
        answer: JudgeletAnswer | None = None,
    ) -> None:
        super().__init__(address)
        self.is_alive_flag = is_alive
        self.answer = answer or JudgeletAnswer(
            score=100,
            verdict="OK",
            protocol={
                "A": GroupProtocolSchema(
                    verdicts=[VerdictSchema(
                        is_successful=True,
                        details="OK",
                        codename="OK",
                    )],
                    score=100,
                    is_successful=True,
                    verdict=VerdictSchema(
                        is_successful=True,
                        details="OK",
                        codename="OK",
                    ),
                ),
            },
            group_scores={"A": 100},
            compilation_error=None,
        )

    async def is_alive(self) -> bool:
        return self.is_alive_flag

    async def check_solution(self, solution: Solution) -> JudgeletAnswer:
        return self.answer


class FakeSolutionGateway(SolutionGateway):
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    async def get_solution_file(self, url: str) -> bytes:
        return self.files[url]
