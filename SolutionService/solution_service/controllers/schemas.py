import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel

from solution_service.application.interfaces.account import UserDTO
from solution_service.domain.entities.abstract import TaskType, SubmissionType


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
    solutions: list[SolutionSchema]
    total_score: int


class StandingsSchema(BaseModel):
    tasks: list[tuple[TaskType, int, str]]
    table: list[UserContestStatusSchema]


class TestCaseResult(BaseModel):
    return_code: int
    stdout: str
    stderr: str
    verdict: str
    is_successful: bool


class MQSolutionAnswer(BaseModel):
    id: str
    score: int
    detailed_verdict: str
    short_verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, list[TestCaseResult]]
    compilation_error: str | None = None
