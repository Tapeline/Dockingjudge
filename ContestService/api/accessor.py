from datetime import timedelta
from typing import Any

from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from api import models
from api.auth import User


def get_object_or_null[Model_T: Model](
    model: type[Model_T], *args: Any, **kwargs: Any,
) -> Model_T | None:
    """Try to get object with given filters or return None."""
    try:
        return get_object_or_404(model, *args, **kwargs)
    except Http404:
        return None


def user_can_apply_for_contest(
    user: User, contest: models.Contest,
) -> bool:
    """Check if user can apply for a contest."""
    return is_contest_open(contest)


def user_applied_for_contest(
    user: int | None, contest: models.Contest,
) -> bool:
    """Check if user has applied for a contest."""
    if not user:
        return False
    return models.ContestSession.objects.filter(
        user=user, contest=contest,
    ).exists()


def user_get_time_left(
    user: int | None, contest: models.Contest,
) -> timedelta | None:
    """Get timedelta of time left to solve the contest."""
    session: models.ContestSession | None = get_object_or_null(
        models.ContestSession,
        user=user, contest=contest,
    )
    if not user:
        return None
    if session is None:
        return None
    time_passed = timezone.now() - session.started_at
    return timedelta(seconds=contest.time_limit_seconds) - time_passed


def user_has_time_left(user: int, contest: models.Contest) -> bool:
    """Check if user has any time left to solve the contest."""
    user_time_left = user_get_time_left(user, contest)
    return (
        contest.time_limit_seconds < 0
        or (user_time_left is not None and user_time_left.total_seconds() > 0)
    )


def is_contest_open(contest: models.Contest) -> bool:
    """Check if contest is open to submissions and applications."""
    return contest.is_started and not contest.is_ended


def purge_objects_of_user(user: int) -> None:
    """Delete all objects belonging to this user."""
    models.Contest.objects.filter(author=user).delete()
    models.ContestSession.objects.filter(user=user).delete()
