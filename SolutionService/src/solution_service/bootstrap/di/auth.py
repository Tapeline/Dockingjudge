from typing import Any

from dishka import Provider, provide, Scope
from litestar import Request

from solution_service.application.exceptions import NotAuthenticated
from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.user import UserIdProvider


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_current_user(
        self, request: Request
    ) -> UserIdProvider:
        return LitestarIdProvider(request.user)


class LitestarIdProvider(UserIdProvider):
    def __init__(self, user: User | None) -> None:
        self.user = user

    async def get_user(self) -> User | None:
        return self.user

    async def require_user(self) -> User:
        if self.user is None:
            raise NotAuthenticated
        return self.user
