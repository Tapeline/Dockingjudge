from enum import Enum
from typing import Any

from django.db.models import Model
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError

from . import models


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


def validate_pages_list(pages: list[dict[str, Any]]) -> None:
    """Ensure pages are defined correctly."""
    for page in pages:
        validate_page_in_list(page)


def validate_page_in_list(page: dict[str, Any]) -> None:
    """Ensure page is defined correctly."""
    if page.get("type") not in ("text", "code", "quiz"):
        raise ValidationError(
            "Invalid page: bad type parameter",
            "INVALID_PAGE_BAD_TYPE_PARAMETER",
        )
    if "id" not in page:
        raise ValidationError(
            "Invalid page: no id",
            "INVALID_PAGE_NO_ID",
        )
    model = {
        "text": models.TextPage,
        "code": models.CodeTask,
        "quiz": models.QuizTask,
    }[page["type"]]
    if not model.objects.filter(id=page["id"]).exists():
        raise ValidationError(
            "Invalid page: id does not exist",
            "INVALID_PAGE_ID_NOT_EXISTS",
        )


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


def validate_task_id_and_get(task_type: str, task_id: int) -> Model:
    """Try to get task of given type and id."""
    if task_type not in ("quiz", "code"):
        raise ValidationError(
            f"Bad task type {task_type}",
            "BAD_TASK_TYPE",
        )
    model = {
        "quiz": models.QuizTask,
        "code": models.CodeTask,
    }[task_type]
    if not model.objects.filter(id=task_id).exists():
        raise ValidationError(
            f"No task of type {task_type} with id {task_id}", "NOT_FOUND",
        )
    return model.objects.get(id=task_id)
