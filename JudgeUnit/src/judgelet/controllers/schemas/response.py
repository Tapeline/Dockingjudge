from pydantic import BaseModel


class TestCaseResult(BaseModel):
    """Result for a test case."""

    return_code: int
    stdout: str
    stderr: str
    verdict: str
    is_successful: bool


class VerdictSchema(BaseModel):
    """Single verdict."""

    codename: str
    is_successful: bool
    details: str


class GroupProtocolSchema(BaseModel):
    """Group run result."""

    score: int
    verdicts: list[VerdictSchema]
    is_successful: bool
    verdict: VerdictSchema


class RunResponse(BaseModel):
    """Response model."""

    score: int
    verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, GroupProtocolSchema]
    compilation_error: str | None = None
