from typing import override

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from contest_service import settings

from . import accessor, models

type AnyPage = models.TextPage | models.QuizTask | models.CodeTask


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
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        if "*" in settings.ALLOW_CONTEST_CREATION_TO:
            return True
        return request.user.username in settings.ALLOW_CONTEST_CREATION_TO


class IsContestAdminOrReadOnly(BasePermission):
    """Grant all rights if admin or read-only otherwise."""

    @override
    def has_object_permission(
        self, request: Request, view: APIView,
        obj: AnyPage | models.Contest,
    ) -> bool:
        if isinstance(obj, models.Contest):
            target = obj
        elif isinstance(
            obj, (models.TextPage, models.QuizTask, models.CodeTask),
        ):
            target = obj.contest
        else:
            raise AssertionError(
                "Invalid obj type for IsContestAdminOrReadOnly"
            )
        return (
            request.method in ("GET", "HEAD", "OPTIONS")
            or target.author == request.user.id
        )


class IsContestAdminOrReadOnlyForParticipants(BasePermission):
    """Grant all rights if admin or read-only if participant."""

    @override
    def has_object_permission(
        self, request: Request, view: APIView,
        obj: AnyPage | models.Contest,
    ) -> bool:
        if isinstance(obj, models.Contest):
            target = obj
        elif isinstance(
            obj, (models.TextPage, models.QuizTask, models.CodeTask),
        ):
            target = obj.contest
        else:
            raise AssertionError(
                "Invalid obj type for IsContestAdminOrReadOnly"
            )
        if request.user.id and not isinstance(obj, models.Contest):
            return (
                request.method in ("GET", "HEAD", "OPTIONS")
                and can_view_this_page(request.user.id, obj)
            ) or target.author == request.user.id
        else:
            return (
                request.method in ("GET", "HEAD", "OPTIONS")
                or target.author == request.user.id
            )
