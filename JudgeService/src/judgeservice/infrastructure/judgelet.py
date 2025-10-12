import base64
from http import HTTPStatus
from typing import Any, override

import aiohttp
import structlog

from judgeservice.config import Config
from judgeservice.domain.entities import (
    Judgelet,
    JudgeletAnswer,
    Solution,
    SubmissionType,
)
from judgeservice.domain.exceptions import (
    BadJudgeletResponseException,
)

logger = structlog.get_logger(__name__)


class JudgeletImpl(Judgelet):
    """Judgelet implementation that works over HTTP."""

    def __init__(
        self,
        address: str,
        config: Config,
    ) -> None:
        super().__init__(address)
        self._endpoint_format = config.judgelet_endpoint_format
        self._timeout = aiohttp.ClientTimeout(
            total=config.pool.consider_dead_after_timeout_s,
        )

    @override
    async def is_alive(self) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.address}/ping",
                    timeout=self._timeout,
                ) as response:
                    return response.status == HTTPStatus.OK
            except TimeoutError:
                return False

    @override
    async def check_solution(self, solution: Solution) -> JudgeletAnswer:
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                self._endpoint_format.format(self.address),
                json=_form_check_request(solution),
            ) as response,
        ):
            logger.info("Got response", status=response.status)
            if response.status not in (200, 201):
                logger.error(
                    "Judgelet answered with an unusual code",
                    judgelet=self.address,
                    status=response.status,
                    response=await response.text(),
                )
                raise BadJudgeletResponseException
            json_response = await response.json()
            return JudgeletAnswer(**json_response)


def _form_check_request(solution: Solution) -> dict[str, Any]:
    if not solution.solution_data:
        logger.error("Solution does not contain data", solution=solution)
        raise AssertionError("Solution does not contain data")
    request: dict[str, str | dict[str, str]] = {
        "id": solution.id,
        "compiler": solution.compiler,
        "suite": solution.suite,
    }
    if solution.submission_type == SubmissionType.STR:
        request["code"] = {
            "type": "str",
            "code": solution.solution_data.decode(errors="ignore"),
        }
    elif solution.submission_type == SubmissionType.ZIP:
        if not solution.main_file:
            logger.error(
                "Solution does not contain main_file", solution=solution,
            )
            raise AssertionError("Solution does not contain main_file")
        request["code"] = {
            "type": "zip",
            "b64": base64.b64encode(solution.solution_data).decode(),
            "main": solution.main_file,
        }
    return request
