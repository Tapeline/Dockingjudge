"""Provides classes for representing and running groups of test cases"""

from judgelet.compilers.abc_compiler import RunResult
from judgelet.testing.tests.testcase import TestCase
from judgelet.testing.validators.abc_validator import ValidatorAnswer
from judgelet import models


class TestGroup:
    """Represents a TestCase group"""
    name: str
    depends_on: list[str]
    test_cases: list[TestCase]
    points: int
    score_only_on_full_pass: bool = False
    default_time_lim: int
    default_mem_lim: int

    def __init__(self, name: str, depends_on: list[str],
                 test_cases: list[TestCase], points: int,
                 default_time_lim: int, default_mem_lim: int,
                 score_only_on_full_pass: bool = False):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-positional-arguments
        self.name = name
        self.depends_on = depends_on
        self.test_cases = test_cases
        self.points = points
        self.score_only_on_full_pass = score_only_on_full_pass
        self.default_mem_lim = default_mem_lim
        self.default_time_lim = default_time_lim

    async def get_result(self, compiler_name: str, file_name: str, solution_dir: str) \
            -> tuple[bool, int, list[tuple[RunResult, ValidatorAnswer]], str]:
        """Run all test cases and calculate the result"""
        passed = 0
        protocol = []
        verdict = None
        for testcase in self.test_cases:
            if testcase.memory_limit_mb is None:
                testcase.memory_limit_mb = self.default_mem_lim
            if testcase.time_limit is None:
                testcase.time_limit = self.default_time_lim
            run_result, result = await testcase.perform_test_case(compiler_name,
                                                                  file_name,
                                                                  solution_dir)
            protocol.append((run_result, result))
            if result.success:
                passed += 1
            elif verdict is None:
                verdict = result.message
        if passed < len(self.test_cases) and self.score_only_on_full_pass:
            return False, 0, protocol, verdict or "OK"
        if passed == len(self.test_cases):
            return True, self.points, protocol, verdict or "OK"
        return (False, int(self.points / len(self.test_cases) * passed),
                protocol, verdict or "OK")

    @staticmethod
    def deserialize(data: models.TestGroup,
                    default_time_limit,
                    default_memory_limit) -> "TestGroup":
        """Create from pydantic"""
        cases = [TestCase.deserialize(case_data)
                 for case_data in data.cases]
        return TestGroup(
            data.name,
            data.depends_on,
            cases,
            data.points,
            default_time_limit, default_memory_limit,
            data.scoring_rule == models.ScoringRuleEnum.POLAR
        )
