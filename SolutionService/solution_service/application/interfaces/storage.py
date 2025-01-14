from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

type URL = str


@dataclass
class File:
    name: str
    contents: bytes
    encoding: str = "UTF-8"

    @property
    def str_contents(self) -> str:
        return self.contents.decode(self.encoding)


class AbstractStorage(ABC):
    @abstractmethod
    async def get_file_url(self, name: str) -> URL:
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, file: File) -> URL:
        raise NotImplementedError


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...
