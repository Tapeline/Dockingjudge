"""Domain entities"""
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass
class QuizCheckerVerdict:
    score: int
    is_successful: bool


type QuizAnswer = str


class AbstractQuizChecker[CheckerParams](ABC):
    """ABC for quiz checkers"""
    name: str
    params: CheckerParams
    all_checkers = {}

    def __init__(self, max_score: int, parameters: CheckerParams):
        self.params: CheckerParams = parameters
        self.max_score = max_score

    def __init_subclass__(cls):
        super().__init_subclass__()
        AbstractQuizChecker.all_checkers[cls.name] = cls

    @abstractmethod
    def check(
            self,
            actual_answer: QuizAnswer
    ) -> QuizCheckerVerdict:
        raise NotImplementedError


class TaskType(Enum):
    QUIZ = "quiz"
    CODE = "code"


@dataclass
class GenericSolution:
    uid: str | None
    contest_id: int
    task_id: int
    task_type: TaskType
    user_id: int
    score: int
    short_verdict: str
    submitted_at: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class QuizSolution(GenericSolution):
    submitted_answer: str = ""
    task_type = TaskType.QUIZ


class SubmissionType(Enum):
    STR = "str"
    ZIP = "zip"


@dataclass
class CodeSolution(GenericSolution):
    type GroupName = str

    task_type = TaskType.CODE
    submission_url: str = ""
    submission_type: SubmissionType = SubmissionType.STR
    compiler_name: str = ""
    main_file: str | None = None
    group_scores: dict[GroupName, int] = field(default_factory=dict)
    detailed_verdict: str = ""


type AnySolution = QuizSolution | CodeSolution
