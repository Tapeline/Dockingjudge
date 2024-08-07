from enum import Enum

from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError

from . import models


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


class TestSuite(BaseModel):
    groups: list[TestGroup]


class QuizValidationType(str, Enum):
    regex = 'regex'
    contains = 'contains'


class QuizValidator(BaseModel):
    type: QuizValidationType
    pattern: str


def validate_pages_list(pages: list):
    for page in pages:
        validate_page_in_list(page)


def validate_page_in_list(page: dict):
    if page.get("type") not in ("text", "code", "quiz"):
        raise ValidationError(
            "Invalid page: bad type parameter",
            "INVALID_PAGE_BAD_TYPE_PARAMETER"
        )
    if "id" not in page:
        raise ValidationError(
            "Invalid page: no id",
            "INVALID_PAGE_NO_ID"
        )
    model = {
        "text": models.TextPage,
        "code": models.CodeTask,
        "quiz": models.QuizTask
    }[page["type"]]
    if not model.filter(id=page["id"]).exists():
        raise ValidationError(
            "Invalid page: id does not exist",
            "INVALID_PAGE_ID_NOT_EXISTS"
        )


def validate_test_suite(test_suite: dict):
    try:
        TestSuite(**test_suite)
    except PydanticValidationError as e:
        raise ValidationError from e


def validate_quiz_validator(validator: dict):
    try:
        QuizValidator(**validator)
    except PydanticValidationError as e:
        raise ValidationError from e
