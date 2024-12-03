"""Provides pydantic models"""


from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ScoringRuleEnum(str, Enum):  # noqa: WPS600 (subclassing str)
    """Determines whether scoring is for a single test or for a full group"""

    POLAR = "polar"
    GRADED = "graded"


class Validator(BaseModel):
    """Output checker"""

    type: str
    args: dict


class TestCase(BaseModel):
    """Test case model"""

    validators: list[Validator]
    stdin: str
    files_in: dict = {}
    files_out: list = []
    time_limit: Optional[int] = None
    mem_limit_mb: Optional[int] = None


class TestGroup(BaseModel):
    """Test group model"""

    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.GRADED
    cases: list[TestCase]


class PrecompileCheckerModel(BaseModel):
    """Checks code before running"""

    type: str
    parameters: dict = {}  # noqa: WPS110 (bad name)


class TestSuite(BaseModel):
    """Test configuration"""

    place_files: Optional[str] = None
    precompile: list[PrecompileCheckerModel]
    groups: list[TestGroup]
    public_cases: list[dict] = []
    time_limit: int
    mem_limit_mb: int
    compile_timeout: int = 5


class RunRequest(BaseModel):
    """Request model"""

    id: str
    code: dict
    compiler: str
    suite: TestSuite


class TestCaseResult(BaseModel):
    """Result for a test case"""

    return_code: int
    stdout: str
    stderr: str
    verdict: str
    is_successful: bool


class RunAnswer(BaseModel):
    """Response model"""

    score: int
    verdict: str
    group_scores: dict[str, int]
    protocol: list[list[TestCaseResult]]
    compilation_error: str | None = None
