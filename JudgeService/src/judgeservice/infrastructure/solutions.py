from http import HTTPStatus
from typing import override

import aiohttp
import structlog
from dishka import FromDishka

from judgeservice.application.interfaces import SolutionGateway
from judgeservice.config import Config

logger = structlog.get_logger(__name__)


class SolutionGatewayImpl(SolutionGateway):
    """Gets solutions from S3."""

    def __init__(self, config: FromDishka[Config]) -> None:
        self.s3_base_url = config.s3.base_url

    @override
    async def get_solution_file(self, url: str) -> bytes:
        async with (
            aiohttp.ClientSession() as session,
            session.get(f"{self.s3_base_url}{url}") as response,
        ):
            if response.status != HTTPStatus.OK:
                response_text = await response.text()
                logger.error(
                    "S3 returned non-200 code",
                    status=response.status,
                    response=response_text,
                )
                raise ValueError(
                    "Solution gateway returned non-200 code",
                    response_text,
                )
            return await response.read()
