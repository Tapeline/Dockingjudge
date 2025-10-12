from judgelet.controllers.schemas.response import (
    GroupProtocolSchema,
    RunResponse,
    VerdictSchema,
)
from judgelet.domain.results import Verdict
from judgelet.domain.test_group import GroupProtocol
from judgelet.domain.test_suite import SuiteResult


def dump_run_response(result: SuiteResult) -> RunResponse:
    """Transform suite result DM to pydantic response."""
    return RunResponse(
        score=result.score,
        verdict=result.verdict.codename,
        protocol={
            group_name: _transform_protocol(protocol)
            for group_name, protocol in result.protocol.items()
        },
        group_scores=result.group_scores,
    )


def _transform_protocol(protocol: GroupProtocol) -> GroupProtocolSchema:
    return GroupProtocolSchema(
        score=protocol.score,
        verdict=_transform_verdict(protocol.verdict),
        verdicts=list(map(_transform_verdict, protocol.verdicts)),
        is_successful=protocol.is_successful,
    )


def _transform_verdict(verdict: Verdict) -> VerdictSchema:
    return VerdictSchema(
        codename=verdict.codename,
        is_successful=verdict.is_successful,
        details=verdict.details,
    )
