"""Contains classes related to test suite."""

from collections.abc import Sequence, Mapping
from functools import partial
from typing import Any

from attrs import frozen

from judgelet.domain.checking import PrecompileChecker
from judgelet.domain.execution import SolutionRunner
from judgelet.domain.results import RunResult, ExitState, Verdict
from judgelet.domain.test_group import TestGroup, GroupProtocol


@frozen
class SuiteResult:
    is_successful: bool
    score: int
    protocol: Mapping[str, GroupProtocol]
    verdict: Verdict
    compilation_error: str | None = None

    @property
    def group_scores(self) -> dict[str, int]:
        return {
            group_name: protocol.score
            for group_name, protocol in self.protocol.items()
        }


class TestSuite:
    """Represents a test suite."""

    def __init__(
            self,
            test_groups: Sequence[TestGroup],
            precompile_checks: Sequence[PrecompileChecker[Any]],
            compilation_timeout_s: float,
            test_group_dependencies: Mapping[str, Sequence[str]],
            additional_files: Mapping[str, str],
            envs: Mapping[str, str]
    ) -> None:
        """Create suite."""
        self.groups = test_groups
        self.precompile_checks = precompile_checks
        self.compilation_timeout_s = compilation_timeout_s
        self.depends = test_group_dependencies
        self.additional_files = additional_files
        self.envs = envs

    async def run(self, runner: SolutionRunner) -> SuiteResult:
        result = await runner.compile(self.compilation_timeout_s)
        if not result.is_successful:
            return _get_suite_result_on_compilation_error(result)
        protocol: dict[str, GroupProtocol] = {}
        total_score: int = 0
        is_successful: bool = True
        verdict = Verdict.OK()
        for group in self.groups:
            group_protocol = await group.run(runner)
            protocol[group.name] = group_protocol
            total_score += group_protocol.score
            is_successful = is_successful and group_protocol.is_successful
            if not group_protocol.is_successful:
                verdict = group_protocol.verdict
        return SuiteResult(
            is_successful=is_successful,
            score=total_score,
            protocol=protocol,
            verdict=verdict
        )


def _get_suite_result_on_compilation_error(error: RunResult) -> SuiteResult:
    factory = lambda err: SuiteResult(
        is_successful=False,
        score=0,
        protocol={},
        verdict=Verdict.CE(err),
        compilation_error=err
    )
    if error.state == ExitState.MEM_LIMIT:
        return factory("compiler memory limit")
    if error.state == ExitState.TIME_LIMIT:
        return factory("compiler time limit")
    return factory(
        f"-- compilation error --\n\n"
        f"{error.stderr}"
    )
