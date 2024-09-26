"""
Request handler
"""

import logging

import aiohttp

from judgeservice import settings
from judgeservice.exceptions import BadRequestFormatException, JudgeletAnswerException


def validate_request(request_data: dict) -> None:
    """Minimal request validation"""
    if "compiler" not in request_data:
        raise BadRequestFormatException


async def handle_request(request_data: dict, target_addr: str) -> dict:
    """Direct request to judgelet and wait for the answer"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
                settings.JUDGELET_ENDPOINT % target_addr,
                json=request_data
        ) as response:
            logging.info("Got response %s", response.status)
            if response.status != 200:
                raise JudgeletAnswerException(await response.json())
            json_response = await response.json()
            return json_response
