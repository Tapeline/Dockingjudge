from enum import StrEnum
from typing import Mapping, Optional, Self

from pydantic import BaseModel, model_validator

from judgelet.domain.test_group import GroupProtocol


class ScoringRuleEnum(StrEnum):
    """Determines whether scoring is for a single test or a full group."""

    POLAR = "polar"
    GRADED = "graded"


class ValidatorSchema(BaseModel):
    """Output checker"""

    type: str
    args: dict


class TestCase(BaseModel):
    """Test case model"""

    validators: list[ValidatorSchema]
    stdin: str
    files_in: dict = {}
    files_out: list = []
    time_limit: Optional[float] = None
    mem_limit_mb: Optional[float] = None


class TestGroupSchema(BaseModel):
    """Test group model"""

    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.GRADED
    cases: list[TestCase]


class PrecompileCheckerSchema(BaseModel):
    """Checks code before running"""

    type: str
    args: dict = {}  # noqa: WPS110 (bad name)


class TestSuite(BaseModel):
    """Test configuration"""

    groups: list[TestGroupSchema]
    precompile: list[PrecompileCheckerSchema]
    time_limit: float
    mem_limit_mb: float
    compile_timeout: int = 5
    place_files: dict[str, str] = {}
    public_cases: list[dict] = []
    envs: dict[str, str] = {}


class SolutionSchema(BaseModel):
    type: str
    code: str | None = None
    b64: str | None = None
    main: str | None = None

    @model_validator(mode='after')
    def validate_type(self) -> Self:
        match self.type:
            case "str":
                if self.code is None:
                    raise ValueError("code should not be None")
            case "zip":
                if self.b64 is None:
                    raise ValueError("b64 should not be None")
                if self.main is None:
                    raise ValueError("main should not be None")
            case _:
                raise ValueError(f"unknown code type {self.type}")
        return self


class RunRequest(BaseModel):
    """Request model"""

    id: str
    code: SolutionSchema
    compiler: str
    suite: TestSuite


class TestCaseResult(BaseModel):
    """Result for a test case"""

    return_code: int
    stdout: str
    stderr: str
    verdict: str
    is_successful: bool


class VerdictSchema(BaseModel):
    codename: str
    is_successful: bool
    details: str


class GroupProtocolSchema(BaseModel):
    score: int
    verdicts: list[VerdictSchema]
    is_successful: bool
    verdict: VerdictSchema


class RunResponse(BaseModel):
    """Response model"""

    score: int
    verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, GroupProtocolSchema]
    compilation_error: str | None = None
