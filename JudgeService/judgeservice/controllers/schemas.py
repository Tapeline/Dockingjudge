from pydantic import BaseModel

from judgeservice.domain.entities import SubmissionType, TestCaseResult


class MQSolutionCheckRequest(BaseModel):
    id: str
    solution_url: str
    main_file: str | None
    submission_type: SubmissionType
    compiler: str
    suite: dict


class MQSolutionAnswer(BaseModel):
    id: str
    score: int
    short_verdict: str
    group_scores: dict[str, int]
    detailed_verdict: str
    protocol: dict[str, list[TestCaseResult]]
