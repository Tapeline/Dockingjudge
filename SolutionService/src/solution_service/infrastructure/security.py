from http import HTTPStatus
from typing import Any, Final, override

import aiohttp
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
from solution_service.config import OuterServicesConfig

provided_security_definitions: Final[dict[str, SecurityScheme]] = {
    "jwt_auth": SecurityScheme(
        type="apiKey",
        name="Authorization",
        security_scheme_in="header",
        bearer_format="jwt",
    ),
}


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
            if response.status != HTTPStatus.OK:
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
