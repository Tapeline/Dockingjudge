from dataclasses import dataclass
from enum import Enum

from solution_service.application.interfaces.account import UserDTO
from solution_service.domain.entities.abstract import (
    AnySolution,
    SubmissionType
)


@dataclass
class EnrichedUserContestStatus:
    user: UserDTO
    tasks_attempted: int
    tasks_solved: int
    solutions: list[AnySolution]
    total_score: int


@dataclass
class NewCodeSolution:
    task_id: int
    submission_type: SubmissionType
    text: str
    compiler: str
    main_file: str | None = None


@dataclass
class NewQuizSolution:
    task_id: int
    text: str


@dataclass
class SolutionCheckResult:
    score: int
    detailed_verdict: str
    short_verdict: str
    group_scores: dict[str, int]
    protocol: dict
