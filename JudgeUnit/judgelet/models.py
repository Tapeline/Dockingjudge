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
    time_limit: Optional[int] = None
    mem_limit_mb: Optional[int] = None


class TestGroup(BaseModel):
    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.graded
    cases: list[TestCase]


class PrecompileCheckerModel(BaseModel):
    type: str
    parameters: dict = {}


class TestSuite(BaseModel):
    place_files: Optional[str] = None
    precompile: list[PrecompileCheckerModel]
    groups: list[TestGroup]
    public_cases: list[dict]
    time_limit: int
    mem_limit_mb: int


class RunRequest(BaseModel):
    id: str
    code: dict
    compiler: str
    suite: TestSuite


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
