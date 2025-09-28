import base64
from typing import Any, assert_never

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, HttpMethod, route
from litestar.exceptions import ValidationException
from structlog import get_logger

from judgelet.application.interactors import CheckSolutionInteractor
from judgelet.application.precompile_checkers import CHECKERS
from judgelet.application.scoring_poilicies import POLICIES
from judgelet.application.validators import VALIDATORS
from judgelet.controllers.schemas import (
    GroupProtocolSchema,
    PrecompileCheckerSchema,
    RunRequest,
    RunResponse,
    ValidatorSchema,
    VerdictSchema,
)
from judgelet.domain.checking import PrecompileChecker, Validator
from judgelet.domain.files import Solution
from judgelet.domain.results import Verdict
from judgelet.domain.test_case import TestCase
from judgelet.domain.test_group import GroupProtocol, TestGroup
from judgelet.domain.test_suite import TestSuite
from judgelet.infrastructure.languages.lang_list import (
    DEFAULT_FILENAMES,
    LANGUAGES,
)
from judgelet.infrastructure.solutions.str_solution import StringSolution
from judgelet.infrastructure.solutions.zip_solution import ZipSolution


class SolutionsController(Controller):
    @route(
        http_method=HttpMethod.GET,
        path="/ping"
    )
    async def ping(self) -> str:
        return "ok"

    @route(
        http_method=HttpMethod.POST,
        path="/run",
    )
    @inject
    async def get_solution(
            self,
            data: RunRequest,
            interactor: FromDishka[CheckSolutionInteractor]
    ) -> RunResponse:
        log = get_logger().bind(solution_id=data.id)
        if data.compiler not in LANGUAGES:
            raise ValidationException(
                f"bad compiler, avaliable: {LANGUAGES.keys()}"
            )
        test_suite = _load_suite(data)
        solution = _load_solution(data)
        log.info("Request transformed")
        result = await interactor(data.compiler, solution, test_suite)
        log.info("Sending response")
        return RunResponse(
            score=result.score,
            verdict=result.verdict.codename,
            protocol={
                group_name: _transform_protocol(protocol)
                for group_name, protocol in result.protocol.items()
            },
            group_scores=result.group_scores
        )


def _load_suite(data: RunRequest) -> TestSuite:
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
                        list(map(_get_validator, case.validators))
                    )
                    for case in group.cases
                ],
                group.points,
                _get_scoring_policy(group.scoring_rule.value)
            )
            for group in data.suite.groups
        ],
        list(map(_get_precompile_checker, data.suite.precompile)),
        data.suite.compile_timeout,
        {group.name: group.depends_on for group in data.suite.groups},
        data.suite.place_files,
        data.suite.envs
    )


def _load_solution(data: RunRequest) -> Solution:
    if data.code.type == "str":
        return StringSolution(
            data.id,
            DEFAULT_FILENAMES[data.compiler],
            data.code.code
        )
    if data.code.type == "zip":
        return ZipSolution(
            data.id,
            base64.b64decode(data.code.b64),
            data.code.main
        )
    assert_never(data.code.type)


def _get_scoring_policy(policy: str):
    if policy not in POLICIES:
        raise ValidationException(f"bad policy {policy}")
    return POLICIES[policy]()


def _get_validator(validator: ValidatorSchema) -> Validator[Any]:
    if validator.type not in VALIDATORS:
        raise ValidationException(f"bad validator {validator.type}")
    validator_cls = VALIDATORS[validator.type]
    return validator_cls(validator_cls.args_cls(**validator.args))


def _get_precompile_checker(
        checker: PrecompileCheckerSchema
) -> PrecompileChecker[Any]:
    if checker.type not in CHECKERS:
        raise ValidationException(f"bad precompile checker {checker.type}")
    checker_cls = CHECKERS[checker.type]
    return checker_cls(checker_cls.args_cls(**checker.args))


def _transform_protocol(protocol: GroupProtocol) -> GroupProtocolSchema:
    return GroupProtocolSchema(
        score=protocol.score,
        verdict=_transform_verdict(protocol.verdict),
        verdicts=list(map(_transform_verdict, protocol.verdicts)),
        is_successful=protocol.is_successful
    )


def _transform_verdict(verdict: Verdict) -> VerdictSchema:
    return VerdictSchema(
        codename=verdict.codename,
        is_successful=verdict.is_successful,
        details=verdict.details
    )
