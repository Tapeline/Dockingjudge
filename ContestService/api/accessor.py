from datetime import timedelta
from typing import Type

from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from . import models


def get_object_or_null(model: Type[Model], *args, **kwargs) -> Model | None:
    """
    Try to get object with given filters or return None
    (instead of raising an error)
    """
    try:
        return get_object_or_404(model, *args, **kwargs)
    except Http404:
        return None


def user_applied_for_contest(user: int, contest) -> bool:
    return models.ContestSession.objects.filter(user=user, contest=contest).exists()


def user_get_time_left(user: int, contest) -> timedelta | None:
    session: models.ContestSession | None = get_object_or_null(
        models.ContestSession,
        user=user, contest=contest
    )
    if session is None:
        return None
    time_passed = timezone.now() - session.started_at
    return timedelta(seconds=contest.time_limit_seconds) - time_passed


def user_has_time_left(user: int, contest) -> bool:
    return user_get_time_left(user, contest).seconds > 0


def is_contest_open(contest) -> bool:
    return contest.is_started and not contest.is_ended
