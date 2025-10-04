from typing import Any


class BadServiceResponseException(Exception):
    def __init__(self, service: str, data: Any) -> None:
        super().__init__(service, data)
        self.service = service
        self.data = data
