from collections.abc import Sequence
from typing import Any

from judgelet.application.scoring_poilicies import GradualScoringPolicy
from judgelet.domain.checking import PrecompileChecker, Validator
from judgelet.domain.results import ExitState, RunResult
from judgelet.domain.test_case import TestCase
from judgelet.domain.test_group import ScoringPolicy, TestGroup
from judgelet.domain.test_suite import TestSuite


def create_suite(
    *group_factories: TestGroup,
    precompile_checks: list[PrecompileChecker[Any]] | None = None,
    group_deps: dict[str, Sequence[str]] | None = None,
    additional_files: dict[str, str] | None = None,
) -> TestSuite:
    return TestSuite(
        test_groups=group_factories,
        precompile_checks=precompile_checks or [],
        compilation_timeout_s=5,
        test_group_dependencies=group_deps or {},
        additional_files=additional_files or {},
        envs={},
    )


def create_group(
    name: str,
    *cases: TestCase,
    score: int = 100,
    scoring_policy: ScoringPolicy | None = None,
) -> TestGroup:
    return TestGroup(
        name=name,
        test_cases=cases,
        full_score=score,
        scoring_policy=scoring_policy or GradualScoringPolicy(),
    )


def create_test(
    *validators: Validator[Any],
    input_files: dict[str, str] | None = None,
    output_files: list[str] | None = None,
) -> TestCase:
    return TestCase(
        stdin="",
        time_limit_s=1,
        memory_limit_mb=256,
        input_files=input_files or {},
        output_files=output_files or [],
        validators=validators,
    )


def create_ok_result(stdout: str) -> RunResult:
    return RunResult(
        stdout=stdout,
        stderr="",
        return_code=0,
        state=ExitState.FINISHED,
    )
