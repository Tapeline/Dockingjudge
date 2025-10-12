from dataclasses import dataclass
from typing import Any

from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.solutions import UserSolutionScore
from solution_service.domain.abstract import AnySolution, SubmissionType


@dataclass
class EnrichedUserContestStatus:
    """UserContestStatus with actual user inside."""

    user: User
    tasks_attempted: int
    tasks_solved: int
    solutions: list[AnySolution]
    total_score: int


@dataclass
class EnrichedUserStandingRow:
    """How well is user doing in the contest."""

    user: User
    tasks_attempted: int
    tasks_solved: int
    solutions: list[UserSolutionScore | None]
    total_score: int


@dataclass
class NewCodeSolution:
    """New code solution."""

    task_id: int
    submission_type: SubmissionType
    text: str
    compiler: str
    main_file: str | None = None


@dataclass
class NewQuizSolution:
    """New quiz solution."""

    task_id: int
    text: str


@dataclass
class SolutionCheckResult:
    """Result of checking a solution."""

    score: int
    detailed_verdict: str
    short_verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, Any]
