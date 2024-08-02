from judgelet.compilers.abc_compiler import RunResult
from judgelet.testing.tests.testcase import TestCase
from judgelet.testing.validators.abc_validator import ValidatorAnswer
from judgelet import models


class TestGroup:
    name: str
    depends_on: list[str]
    test_cases: list[TestCase]
    points: int
    score_only_on_full_pass: bool = False

    def __init__(self, name: str, depends_on: list[str],
                 test_cases: list[TestCase], points: int,
                 score_only_on_full_pass: bool = False):
        self.name = name
        self.depends_on = depends_on
        self.test_cases = test_cases
        self.points = points
        self.score_only_on_full_pass = score_only_on_full_pass

    async def get_result(self, compiler_name: str, file_name: str) \
            -> tuple[bool, int, list[tuple[RunResult, ValidatorAnswer]], str]:
        passed = 0
        protocol = []
        verdict = None
        for testcase in self.test_cases:
            run_result, result = await testcase.perform_test_case(compiler_name, file_name)
            protocol.append((run_result, result))
            if result.success:
                passed += 1
            elif verdict is None:
                verdict = result.message
        if passed < len(self.test_cases) and self.score_only_on_full_pass:
            return False, 0, protocol, verdict or "OK"
        if passed == len(self.test_cases):
            return True, self.points, protocol, verdict or "OK"
        return False, int(self.points / len(self.test_cases) * passed), protocol, verdict or "OK"

    @staticmethod
    def deserialize(data: models.TestGroup) -> "TestGroup":
        cases = [TestCase.deserialize(case_data)
                 for case_data in data.cases]
        return TestGroup(
            data.name,
            data.depends_on,
            cases,
            data.points,
            data.scoring_rule == models.ScoringRuleEnum.polar
        )