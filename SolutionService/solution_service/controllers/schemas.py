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


class SolutionSchema(BaseModel):
    id: str
    task_id: int
    task_type: TaskType
    user_id: int
    score: int
    short_verdict: str
    data: QuizSolutionExtraSchema | CodeSolutionExtraSchema | None


class PostCodeSolutionSchema(BaseModel):
    compiler: str
    submission_type: SubmissionType
    text: str
    main_file: str | None


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


class TestCaseResult(BaseModel):
    return_code: int
    stdout: str
    stderr: str
    verdict: str
    is_successful: bool


class RunAnswer(BaseModel):
    score: int
    verdict: str
    group_scores: dict[str, int]
    protocol: list[list[TestCaseResult]]
    compilation_error: str | None = None


class MQSolutionAnswer(BaseModel):
    answer_to: str
    is_successful: bool
    code: str | None = None
    details: str | None = None
    contents: RunAnswer | None = None
