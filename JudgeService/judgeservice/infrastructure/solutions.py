import aiohttp
from dishka import FromDishka

from judgeservice.application.interfaces import SolutionGateway
from judgeservice.config import Config


class SolutionGatewayImpl(SolutionGateway):
    def __init__(self, config: FromDishka[Config]) -> None:
        self.s3_base_url = config.s3.base_url

    async def get_solution_file(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.s3_base_url}{url}") as response:
                if response.status != 200:
                    raise ValueError(
                        "Solution gateway returned non-200 code",
                        await response.text()
                    )
                return await response.read()
