from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

type URL = str


@dataclass
class File:
    name: str
    contents: bytes
    encoding: str = "UTF-8"

    @property
    def str_contents(self) -> str:
        return self.contents.decode(self.encoding)


class Storage(Protocol):
    @abstractmethod
    async def get_file_url(self, name: str) -> URL:
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, file: File) -> URL:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, url: URL) -> File:
        raise NotImplementedError


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class IdGenerator(Protocol):
    @abstractmethod
    def new_id(self) -> str:
        raise NotImplementedError
