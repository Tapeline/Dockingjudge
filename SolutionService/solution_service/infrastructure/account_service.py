from typing import Sequence, Final

import aiohttp
from dishka import FromDishka
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.openapi.spec import SecurityScheme
from litestar.types import ASGIApp

from solution_service.application.interfaces import account
from solution_service.config import OtherServicesConfig, Config
from solution_service.infrastructure.exceptions import BadServiceResponseException


provided_security_definitions: Final[dict[str, SecurityScheme]] = {
    "jwt_auth": SecurityScheme(
        type="apiKey",
        name="Authorization",
        security_scheme_in="header",
        bearer_format="jwt"
    )
}


class AccountServiceImpl(account.AbstractAccountService):
    def __init__(
            self,
            other_services: FromDishka[Config],
    ):
        self.base_url = other_services.services.account_service

    async def get_users_by_ids(self, ids: Sequence[int]) -> Sequence[account.UserDTO]:
        async with (
            aiohttp.ClientSession() as session,
            session.get(f"{self.base_url}/all", params={"id": ids}) as response,
        ):
            if response.status != 200:
                raise BadServiceResponseException("account", response)
            data = await response.json()
            return [
                account.UserDTO(
                    id=user_data["id"],
                    username=user_data["username"],
                    profile_pic=user_data["profile_pic"],
                    roles=[],  # TODO
                    settings=None
                )
                for user_data in data
            ]


class ServiceAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    def __init__(self, app: ASGIApp, other_services: OtherServicesConfig, **kwargs):
        super().__init__(app, **kwargs)
        self.other_services = other_services

    async def authenticate_request(
            self,
            connection: ASGIConnection,
    ) -> AuthenticationResult:
        auth_header = connection.headers.get("authorization")
        if not auth_header:
            raise NotAuthorizedException()
        async with aiohttp.ClientSession() as session:
            async with session.get(
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
                    user=account.UserDTO(
                        id=data["id"],
                        username=data["username"],
                        settings=data["settings"],
                        profile_pic=data["profile_pic"],
                        roles=[],  # TODO implement roles
                    ),
                )


def authenticated_user_guard(
        connection: ASGIConnection,
        _: BaseRouteHandler,
) -> None:
    if connection.user is None:
        raise NotAuthorizedException()
