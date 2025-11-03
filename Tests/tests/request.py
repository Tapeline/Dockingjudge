import os

import httpx


BASE_URL = os.environ.get("TESTS_BASE_URL", "http://localhost:8888/api")


class DockingjudgeClient(httpx.Client):
    def set_token(self, token: str) -> None:
        self.headers["Authorization"] = f"Bearer {token}"


def new_client() -> DockingjudgeClient:
    return DockingjudgeClient(base_url=BASE_URL)
