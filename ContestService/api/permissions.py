from typing import Final, override

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from api import accessor, models
from contest_service import settings

type AnyPage = models.TextPage | models.QuizTask | models.CodeTask

_SAFE_METHODS: Final = frozenset(("GET", "HEAD", "OPTIONS"))


def can_view_all_pages(user: int | None, contest: models.Contest) -> bool:
    """Check if user can view all pages of a contest."""
    return (
        accessor.user_applied_for_contest(user, contest)
        or contest.author == user
    )


def can_view_this_page(
    user: int, page: AnyPage,
) -> bool:
    """Check if user can view this page of a contest."""
    if isinstance(page, models.TextPage) and page.is_enter_page:
        return True
    return can_view_all_pages(user, page.contest)


def can_manage_contest(user: int | None, contest: models.Contest) -> bool:
    """Check if user can manage this contest."""
    return contest.author == user


class CanCreateContest(BasePermission):
    """Grant contest creation rights if user is allowed to create contest."""

    @override
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in _SAFE_METHODS:
            return True
        if "*" in settings.ALLOW_CONTEST_CREATION_TO:
            return True
        return request.user.username in settings.ALLOW_CONTEST_CREATION_TO


class IsContestAdminOrReadOnly(BasePermission):
    """Grant all rights if admin or read-only otherwise."""

    @override
    def has_object_permission(
        self, request: Request, view: APIView,
        page_or_contest: AnyPage | models.Contest,
    ) -> bool:
        if isinstance(page_or_contest, models.Contest):
            target = page_or_contest
        elif isinstance(
            page_or_contest,
            (models.TextPage, models.QuizTask, models.CodeTask),
        ):
            target = page_or_contest.contest
        else:
            raise TypeError(
                "Invalid obj type for IsContestAdminOrReadOnly",
            )
        return (
            request.method in _SAFE_METHODS
            or target.author == request.user.id
        )


class IsContestAdminOrReadOnlyForParticipants(BasePermission):
    """Grant all rights if admin or read-only if participant."""

    @override
    def has_object_permission(
        self, request: Request, view: APIView,
        page_or_contest: AnyPage | models.Contest,
    ) -> bool:
        if isinstance(page_or_contest, models.Contest):
            target = page_or_contest
        elif isinstance(
            page_or_contest,
            (models.TextPage, models.QuizTask, models.CodeTask),
        ):
            target = page_or_contest.contest
        else:
            raise TypeError(
                "Invalid obj type for IsContestAdminOrReadOnly",
            )
        if request.user.id and not isinstance(page_or_contest, models.Contest):
            return (
                request.method in _SAFE_METHODS
                and can_view_this_page(request.user.id, page_or_contest)
            ) or target.author == request.user.id
        return (
            request.method in _SAFE_METHODS
            or target.author == request.user.id
        )
