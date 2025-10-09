from typing import Union

from rest_framework.permissions import BasePermission

from contest_service import settings
from . import accessor, models


def can_view_all_pages(user: int, contest):
    return accessor.user_applied_for_contest(user, contest) or \
        contest.author == user


def can_view_this_page(user: int, page: Union[models.TextPage, models.QuizTask, models.CodeTask]):
    if isinstance(page, models.TextPage) and page.is_enter_page:
        return True
    return can_view_all_pages(user, page.contest)


def can_manage_contest(user: int, contest) -> bool:
    return contest.author == user


class CanCreateContest(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        if "*" in settings.ALLOW_CONTEST_CREATION_TO:
            return True
        return request.user.username in settings.ALLOW_CONTEST_CREATION_TO


class IsContestAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        target = obj
        if isinstance(obj, (models.TextPage, models.QuizTask, models.CodeTask)):
            target = obj.contest
        return (
                (request.method in ('GET', 'HEAD', 'OPTIONS'))
                or
                (target.author == request.user.id)
        )


class IsContestAdminOrReadOnlyForParticipants(BasePermission):
    def has_object_permission(self, request, view, obj):
        target = obj
        if isinstance(obj, (models.TextPage, models.QuizTask, models.CodeTask)):
            target = obj.contest
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS')
            and
            can_view_this_page(request.user.id, obj)
        ) or target.author == request.user.id
