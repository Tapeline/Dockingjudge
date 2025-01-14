from enum import Enum
from typing import Annotated

from pydantic import BaseModel

from solution_service.application.interfaces.account import UserDTO
from solution_service.domain.entities.abstract import TaskType


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


class SubmissionType(Enum):
    STR = "str"
    ZIP = "zip"


class PostCodeSolutionSchema(BaseModel):
    compiler: str
    submission_type: SubmissionType
    text: str


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
