"""
Provides classes for representing and running
test suites - collections of test groups
"""

from judgelet.compilers.abc_compiler import RunResult, AbstractCompiler, UtilityRunResult
from judgelet.testing.precompile.abc_precompile_checker import AbstractPrecompileChecker
from judgelet.testing.tests.testgroup import TestGroup
from judgelet.testing.validators.abc_validator import ValidatorAnswer
from judgelet import models

SuiteResult = tuple[
    Score := int,
    FullProtocol := list[
        GroupProtocol := list[
            TestProtocol := tuple[RunResult, ValidatorAnswer]]],
    GroupScores := dict[GroupName := str, Score],
    Verdict := str
]


class TestSuite:
    """Represents a test suite"""
    groups: list[TestGroup]
    group_dependencies: dict[TargetGroup := str, Dependencies := set[str]]
    default_time_lim: int
    default_mem_lim: int

    def __init__(self,
                 groups: list[TestGroup],
                 group_dependencies: dict[str, set[str]],
                 precompile_checks: list[AbstractPrecompileChecker],
                 default_time_lim: int, default_mem_lim: int):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-positional-arguments
        self.groups = groups
        self.group_dependencies = group_dependencies
        self.precompile_checks = precompile_checks
        self.default_time_lim = default_time_lim
        self.default_mem_lim = default_mem_lim

    async def run_suite(self, compiler_name: str, file_name: str,
                        solution_dir: str, file_names: list[str]) -> SuiteResult:
        """Run precompile checks and run tests"""
        is_precompile_ok = await self.run_precompile_checks(solution_dir, file_names)
        if not is_precompile_ok:
            return 0, [], {g.name: 0 for g in self.groups}, "PCF"
        result = await self.compile(compiler_name, file_name, solution_dir)
        if not result.success:
            return 0, [], {g.name: 0 for g in self.groups}, "CE"
        return await self.run_tests(compiler_name, file_name, solution_dir)

    async def run_precompile_checks(self, solution_dir: str, file_names: list[str]) -> bool:
        # pylint: disable=missing-function-docstring
        for checker in self.precompile_checks:
            if not await checker.perform_check(solution_dir, file_names):
                return False
        return True

    async def compile(self, compiler_name: str,
                      file_name: str, solution_dir: str) -> UtilityRunResult:
        if compiler_name not in AbstractCompiler.COMPILERS:
            return ValidatorAnswer.err("Compiler not found")
        compiler: AbstractCompiler = AbstractCompiler.COMPILERS[compiler_name]()
        result = await compiler.prepare(file_name, solution_dir)
        if not result.success:
            return result
        return await compiler.compile(file_name, solution_dir)

    async def run_tests(self, compiler_name: str, file_name: str, solution_dir: str) \
            -> tuple[int, list[list[tuple[RunResult, ValidatorAnswer]]], dict, str]:
        """Run all groups and calculate result"""
        score = 0
        fully_passed = set()
        full_protocol = []
        group_scores = {}
        verdict = None
        for group in self.groups:
            has_passed, group_score, group_protocol, group_verdict = \
                await group.get_result(compiler_name, file_name, solution_dir)
            full_protocol.append(group_protocol)
            if group.name not in self.group_dependencies:
                fully_passed.add(group.name)
                score += group_score
                group_scores[group.name] = group_score
            elif all(dep in fully_passed for dep in self.group_dependencies[group.name]):
                fully_passed.add(group.name)
                score += group_score
                group_scores[group.name] = group_score
            if not has_passed and verdict is None:
                verdict = group_verdict
        return score, full_protocol, group_scores, verdict or "OK"

    @staticmethod
    def deserialize(data: models.TestSuite) -> "TestSuite":
        """Create from pydantic"""
        groups = [
            TestGroup.deserialize(group, data.time_limit, data.mem_limit_mb)
            for group in data.groups
        ]
        deps = {group.name: set() for group in groups}
        for group in groups:
            for dep in group.depends_on:
                deps[group.name].add(dep)
        precompile = [
            AbstractPrecompileChecker.deserialize(checker)
            for checker in data.precompile
        ]
        return TestSuite(groups, deps, precompile, data.time_limit, data.mem_limit_mb)
