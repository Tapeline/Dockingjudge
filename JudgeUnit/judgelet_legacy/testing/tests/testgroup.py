"""Provides classes for representing and running groups of test cases"""

from judgelet import models
from judgelet.compilers.abc_compiler import RunResult
from judgelet.testing.tests.testcase import TestCase
from judgelet.testing.validators.abc_validator import ValidatorAnswer

TestGroupProtocol = list[tuple[RunResult, ValidatorAnswer]]
Verdict = str
Score = int
HasFullyPassed = bool


class TestGroup:  # noqa: WPS230 (too many attrs)
    """Represents a TestCase group"""

    def __init__(  # noqa: WPS211 (too many args)
            self,
            name: str,
            depends_on: list[str],
            test_cases: list[TestCase],
            points: int,
            default_time_lim: int,
            default_mem_lim: int,
            score_only_on_full_pass: bool = False
    ):
        """Create a test group"""
        self.name = name
        self.depends_on = depends_on
        self.test_cases = test_cases
        self.points = points
        self.score_only_on_full_pass = score_only_on_full_pass
        self.default_mem_lim = default_mem_lim
        self.default_time_lim = default_time_lim
        self._passed = 0
        self._protocol = []
        self._verdict = None

    async def get_result(
            self,
            context,
            compiler_name: str,
            file_name: str,
            solution_dir: str
    ) -> tuple[HasFullyPassed, Score, TestGroupProtocol, Verdict]:
        """Run all test cases and calculate the result"""
        self._passed = 0
        self._protocol = []
        self._verdict = None
        for testcase in self.test_cases:
            await self._run_testcase(
                compiler_name,
                context,
                file_name,
                solution_dir,
                testcase
            )
        return self._determine_final_result()

    async def _run_testcase(  # noqa: WPS211 (too many args)
            self,
            compiler_name,
            context,
            file_name,
            solution_dir,
            testcase
    ) -> None:
        """Run single testcase"""
        self._default_limits_if_not_present(testcase)
        run_result, validator_answer = await testcase.perform_test_case(
            context,
            compiler_name,
            file_name,
            solution_dir
        )
        self._protocol.append((run_result, validator_answer))
        if validator_answer.success:
            self._passed += 1
        elif self._verdict is None:
            self._verdict = validator_answer.message

    def _default_limits_if_not_present(self, testcase) -> None:
        """Set limits for testcase if one does not provide so"""
        if testcase.memory_limit_mb is None:
            testcase.memory_limit_mb = self.default_mem_lim
        if testcase.time_limit is None:
            testcase.time_limit = self.default_time_lim

    def _determine_final_result(self) -> tuple[HasFullyPassed, Score, TestGroupProtocol, Verdict]:
        """Get final score and verdict based on test results"""
        if self._passed < len(self.test_cases) and self.score_only_on_full_pass:
            return False, 0, self._protocol, self._verdict or "OK"

        if self._passed == len(self.test_cases):
            return True, self.points, self._protocol, self._verdict or "OK"

        return (
            False,
            int(self.points / len(self.test_cases) * self._passed),
            self._protocol,
            self._verdict or "OK"
        )

    @staticmethod
    def deserialize(
            model: models.TestGroup,
            default_time_limit,
            default_memory_limit
    ) -> "TestGroup":
        """Create from pydantic"""
        cases = [TestCase.deserialize(case_data)
                 for case_data in model.cases]
        return TestGroup(
            model.name,
            model.depends_on,
            cases,
            model.points,
            default_time_limit,
            default_memory_limit,
            model.scoring_rule == models.ScoringRuleEnum.POLAR
        )
