from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, model_validator


class ScoringRuleEnum(StrEnum):
    """Determines whether scoring is for a single test or a full group."""

    POLAR = "polar"
    GRADED = "graded"


class ValidatorSchema(BaseModel):
    """Output checker."""

    type: str
    args: dict[str, Any]


class TestCase(BaseModel):
    """Test case model."""

    validators: list[ValidatorSchema]
    stdin: str
    files_in: dict[str, str] = {}
    files_out: list[str] = []
    time_limit: float | None = None
    mem_limit_mb: float | None = None


class TestGroupSchema(BaseModel):
    """Test group model."""

    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.GRADED
    cases: list[TestCase]


class PrecompileCheckerSchema(BaseModel):
    """Checks code before running."""

    type: str
    args: dict[str, Any] = {}  # noqa: WPS110 (bad name)


class TestSuite(BaseModel):
    """Test configuration."""

    groups: list[TestGroupSchema]
    precompile: list[PrecompileCheckerSchema]
    time_limit: float
    mem_limit_mb: float
    compile_timeout: int = 5
    place_files: dict[str, str] = {}
    public_cases: list[dict[str, str]] = []
    envs: dict[str, str] = {}


class SolutionSchema(BaseModel):
    """
    Solution spec.

    Either {type = "str", code: str}
    or {type = "zip", b64: str, main: str}

    """

    type: str
    code: str | None = None
    b64: str | None = None
    main: str | None = None

    @model_validator(mode="after")
    def validate_type(self) -> Self:  # noqa: WPS
        """Ensure variants are valid."""
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
    """Request model."""

    id: str
    code: SolutionSchema
    compiler: str
    suite: TestSuite
