"""
Provides classes for representing and running
test suites - collections of test groups
"""
from collections import namedtuple

from judgelet import models
from judgelet.compilers.abc_compiler import AbstractCompiler, UtilityRunResult
from judgelet.testing.precompile.abc_precompile_checker import \
    AbstractPrecompileChecker
from judgelet.testing.tests.testgroup import TestGroup
from judgelet.testing.validators.abc_validator import ValidatorAnswer

SuiteResult = namedtuple(
    "SuiteResult",
    ["score", "protocol", "group_scores", "verdict", "compilation_error"]
)


class TestSuite:  # noqa: WPS230 (too many attrs)
    """Represents a test suite"""

    def __init__(  # noqa: WPS211 (too many args)
            self,
            groups: list[TestGroup],
            group_dependencies: dict[str, set[str]],
            precompile_checks: list[AbstractPrecompileChecker],
            default_time_lim: int,
            default_mem_lim: int,
            compile_timeout: int
    ):
        """Create test suite"""
        self.groups = groups
        self.group_dependencies = group_dependencies
        self.precompile_checks = precompile_checks
        self.default_time_lim = default_time_lim
        self.default_mem_lim = default_mem_lim
        self.compile_timeout = compile_timeout
        self.context = {}

    async def run_suite(
            self,
            compiler_name: str,
            file_name: str,
            solution_dir: str,
            file_names: list[str]
    ) -> SuiteResult:
        """Run precompile checks and run tests"""
        is_precompile_ok = await self._run_precompile_checks(solution_dir, file_names)
        if not is_precompile_ok:
            return SuiteResult(
                score=0,
                protocol=[],
                group_scores={group.name: 0 for group in self.groups},
                verdict="PCF",
                compilation_error=None
            )
        compilation_result = await self._compile(
            compiler_name,
            file_name,
            solution_dir,
            self.compile_timeout
        )
        if not compilation_result.success:
            return SuiteResult(
                score=0,
                protocol=[],
                group_scores={group.name: 0 for group in self.groups},
                verdict=compilation_result.verdict,
                compilation_error=compilation_result.message
            )
        return await self._run_tests(compiler_name, file_name, solution_dir)

    async def _run_precompile_checks(self, solution_dir: str, file_names: list[str]) -> bool:
        """
        Run all precompile checks
        Returns:
            whether checks were successful or not
        """
        for checker in self.precompile_checks:
            if not await checker.perform_check(solution_dir, file_names):
                return False
        return True

    async def _compile(
            self,
            compiler_name: str,
            file_name: str,
            solution_dir: str,
            compile_timeout: int
    ) -> UtilityRunResult:
        """Compile solution"""
        if compiler_name not in AbstractCompiler.COMPILERS:
            return ValidatorAnswer.err("Compiler not found")
        compiler: AbstractCompiler = AbstractCompiler.COMPILERS[compiler_name](self.context)
        preparation_result = await compiler.prepare(file_name, solution_dir)
        if not preparation_result.success:
            return preparation_result
        return await compiler.compile(file_name, compile_timeout, solution_dir)

    async def _run_tests(
            self,
            compiler_name: str,
            file_name: str,
            solution_dir: str
    ) -> SuiteResult:
        """Run all groups and calculate result"""
        score = 0
        fully_passed = set()
        full_protocol = []
        group_scores = {}
        verdict = None
        for group in self.groups:
            (
                has_passed,
                group_score,
                group_protocol,
                group_verdict
            ) = await group.get_result(
                self.context,
                compiler_name,
                file_name,
                solution_dir
            )
            full_protocol.append(group_protocol)
            if self._all_dependencies_passed(fully_passed, group):
                if has_passed:
                    fully_passed.add(group.name)
                score += group_score
                group_scores[group.name] = group_score
            if not has_passed and verdict is None:
                verdict = group_verdict
        return SuiteResult(score, full_protocol, group_scores, verdict or "OK", None)

    def _all_dependencies_passed(self, fully_passed, group):
        if group.name not in self.group_dependencies:
            return True
        return all(dep in fully_passed for dep in self.group_dependencies[group.name])

    @staticmethod
    def deserialize(model: models.TestSuite) -> "TestSuite":
        """Create from pydantic"""
        groups = [
            TestGroup.deserialize(group, model.time_limit, model.mem_limit_mb)
            for group in model.groups
        ]
        deps = {group.name: set() for group in groups}
        for group in groups:
            for dep in group.depends_on:
                deps[group.name].add(dep)
        precompile = [
            AbstractPrecompileChecker.deserialize(checker)
            for checker in model.precompile
        ]
        return TestSuite(
            groups,
            deps,
            precompile,
            model.time_limit,
            model.mem_limit_mb,
            model.compile_timeout
        )
