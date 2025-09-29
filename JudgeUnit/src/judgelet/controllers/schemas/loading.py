import base64
from typing import Any

from litestar.exceptions import ValidationException

from judgelet.application.precompile_checkers import CHECKERS
from judgelet.application.scoring_poilicies import POLICIES
from judgelet.application.validators import VALIDATORS
from judgelet.controllers.schemas.request import (
    PrecompileCheckerSchema,
    RunRequest,
    ValidatorSchema,
)
from judgelet.domain.checking import PrecompileChecker, Validator
from judgelet.domain.files import Solution
from judgelet.domain.test_case import TestCase
from judgelet.domain.test_group import ScoringPolicy, TestGroup
from judgelet.domain.test_suite import TestSuite
from judgelet.infrastructure.languages.lang_list import DEFAULT_FILENAMES
from judgelet.infrastructure.solutions.str_solution import StringSolution
from judgelet.infrastructure.solutions.zip_solution import ZipSolution


def load_suite(data: RunRequest) -> TestSuite:
    """Transform pydantic request into test suite DM."""
    return TestSuite(
        [
            TestGroup(
                group.name,
                [
                    TestCase(
                        case.stdin,
                        case.time_limit or data.suite.time_limit,
                        case.mem_limit_mb or data.suite.mem_limit_mb,
                        case.files_in,
                        case.files_out,
                        list(map(_get_validator, case.validators)),
                    )
                    for case in group.cases
                ],
                group.points,
                _get_scoring_policy(group.scoring_rule.value),
            )
            for group in data.suite.groups
        ],
        list(map(_get_precompile_checker, data.suite.precompile)),
        data.suite.compile_timeout,
        {group.name: group.depends_on for group in data.suite.groups},
        data.suite.place_files,
        data.suite.envs,
    )


def _get_scoring_policy(policy: str) -> ScoringPolicy:
    if policy not in POLICIES:
        raise ValidationException(f"bad policy {policy}")
    return POLICIES[policy]()


def _get_validator(validator: ValidatorSchema) -> Validator[Any]:
    if validator.type not in VALIDATORS:
        raise ValidationException(f"bad validator {validator.type}")
    validator_cls = VALIDATORS[validator.type]
    return validator_cls(validator_cls.args_cls(**validator.args))


def _get_precompile_checker(
        checker: PrecompileCheckerSchema,
) -> PrecompileChecker[Any]:
    if checker.type not in CHECKERS:
        raise ValidationException(f"bad precompile checker {checker.type}")
    checker_cls = CHECKERS[checker.type]
    return checker_cls(checker_cls.args_cls(**checker.args))


def load_solution(data: RunRequest) -> Solution:
    """Transform pydantic solution model into solution DM."""
    # TODO: maybe refactor this using match
    if data.code.type == "str":
        return StringSolution(
            data.id,
            DEFAULT_FILENAMES[data.compiler],
            data.code.code,  # type: ignore[arg-type]
        )
    if data.code.type == "zip":
        return ZipSolution(
            data.id,
            base64.b64decode(data.code.b64),  # type: ignore[arg-type]
            data.code.main,  # type: ignore[arg-type]
        )
    raise AssertionError("unknown solution type", data.code.type)
