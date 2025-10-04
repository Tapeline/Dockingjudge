import logging
from collections.abc import Sequence
from typing import Any, Final, override

import aiohttp
from dishka import FromDishka
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from litestar.openapi.spec import SecurityScheme
from litestar.types import ASGIApp

from solution_service.application.interfaces import account
from solution_service.config import Config, OuterServicesConfig
from solution_service.infrastructure.exceptions import (
    BadServiceResponseException,
)

provided_security_definitions: Final[dict[str, SecurityScheme]] = {
    "jwt_auth": SecurityScheme(
        type="apiKey",
        name="Authorization",
        security_scheme_in="header",
        bearer_format="jwt",
    ),
}


class AccountServiceImpl(account.AccountService):
    def __init__(
            self,
            other_services: FromDishka[Config],
    ) -> None:
        self.base_url = other_services.services.account_service
        self.logger = logging.getLogger("account_service")

    @override
    async def get_users_by_ids(
        self, ids: Sequence[int],
    ) -> Sequence[account.User]:
        self.logger.info("Getting all users")
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.base_url}/all", params={"id": ids},
            ) as response,
        ):
            if response.status != 200:
                self.logger.error(
                    "/all responded %s: %s",
                    response.status, await response.text(),
                )
                raise BadServiceResponseException("account", response)
            data = await response.json()
            return [
                account.User(
                    id=user_data["id"],
                    username=user_data["username"],
                    profile_pic=user_data["profile_pic"],
                    roles=[],  # TODO: implement roles in future
                    settings=None,
                )
                for user_data in data
            ]


class ServiceAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        other_services: OuterServicesConfig,
        **kwargs: Any,
    ) -> None:
        super().__init__(app, **kwargs)
        self.other_services = other_services

    @override
    async def authenticate_request(
        self,
        connection: ASGIConnection[Any, Any, Any, Any],
    ) -> AuthenticationResult:
        auth_header = connection.headers.get("authorization")
        if not auth_header:
            raise NotAuthorizedException
        async with aiohttp.ClientSession() as session, session.get(
            f"{self.other_services.account_service}/authorize",
            headers={
                "Authorization": auth_header,
            },
        ) as response:
            if response.status != 200:
                return AuthenticationResult(
                    auth=None,
                    user=None,
                )
            data = await response.json()
            return AuthenticationResult(
                auth=None,
                user=account.User(
                    id=data["id"],
                    username=data["username"],
                    settings=data["settings"],
                    profile_pic=data["profile_pic"],
                    roles=[],  # TODO: implement roles
                ),
            )


def authenticated_user_guard(
        connection: ASGIConnection[Any, Any, Any, Any],
        _: BaseRouteHandler,
) -> None:
    if connection.user is None:
        raise NotAuthorizedException
