from typing import Any, override

from django.db.models.query import QuerySet

from django.core.exceptions import ValidationError
from django.db import models

from . import validation


def purge_objects_of_user(user: int) -> None:
    """Delete all objects belonging to this user."""
    Contest.objects.filter(author=user).delete()
    ContestSession.objects.filter(user=user).delete()


class Contest(models.Model):
    """Resembles a contest."""

    name = models.CharField(max_length=255)
    author = models.IntegerField()
    description = models.TextField()
    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    time_limit_seconds = models.IntegerField(default=-1)
    pages = models.JSONField(default=list)

    @override
    def save(self, **kwargs: Any) -> None:
        """Validate and save."""
        validate_pages_list(self.pages)
        super().save(**kwargs)


class ContestSession(models.Model):
    """A session for a user on a specific contest."""

    user = models.IntegerField()
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)


class TextPage(models.Model):
    """A single text page (no task)."""

    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text = models.TextField()
    is_enter_page = models.BooleanField(default=False)


class CodeTask(models.Model):
    """A single code task."""

    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    test_suite = models.JSONField()

    @override
    def save(self, **kwargs: Any) -> None:
        """Validate and save."""
        validation.validate_test_suite(self.test_suite)
        super().save(**kwargs)


class QuizTask(models.Model):
    """A single quiz task."""

    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    validator = models.JSONField(default=dict)
    points = models.IntegerField()

    @override
    def save(self, **kwargs: Any) -> None:
        """Validate and save."""
        validation.validate_quiz_validator(self.validator)
        super().save(**kwargs)


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
    query: QuerySet[Any, Any]
    if page["type"] == "text":
        query = TextPage.objects.filter(id=page["id"])
    elif page["type"] == "code":
        query = CodeTask.objects.filter(id=page["id"])
    elif page["type"] == "quiz":
        query = QuizTask.objects.filter(id=page["id"])
    else:
        raise ValidationError("Invalid page type")
    if not query.exists():
        raise ValidationError(
            "Invalid page: id does not exist",
            "INVALID_PAGE_ID_NOT_EXISTS",
        )
