import datetime

from pydantic import BaseModel

from solution_service.domain.abstract import TaskType, SubmissionType


class QuizSolutionExtraSchema(BaseModel):
    submitted_answer: str


class CodeSolutionExtraSchema(BaseModel):
    submission_url: str
    group_scores: dict[str, int] = {}
    detailed_verdict: str
    compiler: str


class SolutionSchema(BaseModel):
    id: str
    task_id: int
    task_type: TaskType
    user_id: int
    score: int
    short_verdict: str
    submitted_at: datetime.datetime
    data: QuizSolutionExtraSchema | CodeSolutionExtraSchema | None


class PostCodeSolutionSchema(BaseModel):
    compiler: str
    submission_type: SubmissionType
    text: str
    main_file: str | None = None


class PostQuizSolutionSchema(BaseModel):
    text: str


class UserSchema(BaseModel):
    id: int
    username: str
    profile_pic: str | None
    roles: list[str]


class UserContestStatusSchema(BaseModel):
    user: UserSchema
    tasks_attempted: int
    tasks_solved: int
    solutions: list[SolutionSchema | None]
    total_score: int


class StandingsSchema(BaseModel):
    tasks: list[tuple[TaskType, int, str]]
    table: list[UserContestStatusSchema]


class VerdictSchema(BaseModel):
    codename: str
    is_successful: bool
    details: str


class GroupProtocolSchema(BaseModel):
    score: int
    verdicts: list[VerdictSchema]
    is_successful: bool
    verdict: VerdictSchema


class MQSolutionAnswer(BaseModel):
    id: str
    score: int
    detailed_verdict: str
    short_verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, GroupProtocolSchema]
    compilation_error: str | None = None


class MQUserEventTarget(BaseModel):
    id: int


class MQUserEvent(BaseModel):
    event: str
    object: MQUserEventTarget


class MQContestEventTargetPage(BaseModel):
    id: int
    type: TaskType


class MQContestEventTarget(BaseModel):
    id: int
    pages: list[MQContestEventTargetPage]


class MQContestEvent(BaseModel):
    event: str
    object: MQContestEventTarget


class MQTaskEventTarget(BaseModel):
    id: int


class MQTaskEvent(BaseModel):
    event: str
    object: MQUserEventTarget
