from typing import Any

from pydantic import BaseModel

from judgeservice.domain.entities import (
    GroupProtocolSchema,
    SubmissionType,
)


class MQSolutionCheckRequest(BaseModel):
    """Request to check a solution."""

    id: str
    solution_url: str
    main_file: str | None
    submission_type: SubmissionType
    compiler: str
    suite: dict[str, Any]


class MQSolutionAnswer(BaseModel):
    """Checked solution answer."""

    id: str
    score: int
    short_verdict: str
    group_scores: dict[str, int]
    detailed_verdict: str
    protocol: dict[str, GroupProtocolSchema]
