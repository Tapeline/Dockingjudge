import logging
from collections.abc import Sequence
from http import HTTPStatus
from typing import override

import aiohttp
from dishka import FromDishka

from solution_service.application.interfaces import account
from solution_service.config import Config
from solution_service.infrastructure.exceptions import (
    BadServiceResponseException,
)


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
            if response.status != HTTPStatus.OK:
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
