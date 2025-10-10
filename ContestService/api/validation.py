from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError


class ScoringRuleEnum(str, Enum):
    """Scoring rule."""

    polar = "polar"
    graded = "graded"


class Validator(BaseModel):
    """Test case validator."""

    type: str
    args: dict


class TestCase(BaseModel):
    """A single test case."""

    validators: list[Validator]
    stdin: str
    files_in: dict = {}
    files_out: list = []
    time_limit: float | None = None
    mem_limit_mb: float | None = None


class TestGroup(BaseModel):
    """A single test group."""

    name: str
    depends_on: list[str] = []
    points: int
    scoring_rule: ScoringRuleEnum = ScoringRuleEnum.graded
    cases: list[TestCase]


class PrecompileCheckerModel(BaseModel):
    """Precompile checker model."""

    type: str
    args: dict


class TestSuite(BaseModel):
    """Test suite."""

    place_files: dict[str, str] = {}
    precompile: list[PrecompileCheckerModel]
    groups: list[TestGroup]
    public_cases: list[dict[str, str]]
    time_limit: float
    mem_limit_mb: float
    compile_timeout: int


class QuizValidator(BaseModel):
    """Quiz task validator."""

    type: str
    args: dict


def validate_test_suite(test_suite: dict[str, Any]) -> None:
    """Validate a code task test suite schema."""
    try:
        TestSuite(**test_suite)
    except PydanticValidationError as e:
        raise ValidationError(detail=e.json()) from e


def validate_quiz_validator(validator: dict[str, Any]) -> None:
    """Validate a quiz task validator schema."""
    try:
        QuizValidator(**validator)
    except PydanticValidationError as e:
        raise ValidationError from e


