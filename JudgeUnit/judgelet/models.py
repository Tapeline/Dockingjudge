from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ScoringRuleEnum(str, Enum):
    polar = 'polar'
    graded = 'graded'


class Validator(BaseModel):
    type: str
    args: dict


class TestCase(BaseModel):
    validators: list[Validator]
    stdin: str
    files_in: dict = {}
    files_out: list = []
    time_limit: int
    mem_limit_mb: int


class TestGroup(BaseModel):
    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.graded
    cases: list[TestCase]


class RunRequest(BaseModel):
    id: Optional[str]
    code: str
    compiler: str
    suite: list[TestGroup]


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

