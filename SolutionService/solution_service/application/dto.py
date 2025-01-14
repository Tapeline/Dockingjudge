from dataclasses import dataclass
from enum import Enum

from solution_service.application.interfaces.account import UserDTO
from solution_service.application.interfaces.solutions import UserContestStatus
from solution_service.domain.entities.abstract import AnySolution, TaskType


@dataclass
class EnrichedUserContestStatus:
    user: UserDTO
    tasks_attempted: int
    tasks_solved: int
    solutions: list[AnySolution]
    total_score: int


@dataclass
class NewCodeSolution:
    class SubmissionType(Enum):
        STR = "str"
        ZIP = "zip"

    task_id: int
    submission_type: SubmissionType
    text: str
    compiler: str


@dataclass
class NewQuizSolution:
    task_id: int
    text: str
