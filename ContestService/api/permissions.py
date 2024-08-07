from typing import Union

from rest_framework.permissions import BasePermission

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


class IsContestAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                (request.method in ('GET', 'HEAD', 'OPTIONS'))
                or
                (obj.owner == request.user.id)
        )


class IsContestAdminOrReadOnlyForParticipants(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS')
            and
            can_view_this_page(request.user.id, obj)
        ) or obj.owner == request.user.id
