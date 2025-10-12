from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

type URL = str


@dataclass
class File:
    """Represents a file."""
    name: str
    contents: bytes
    encoding: str = "UTF-8"

    @property
    def str_contents(self) -> str:
        """Returns the file contents as a string."""
        return self.contents.decode(self.encoding)


class Storage(Protocol):
    """An interface for a file storage."""

    @abstractmethod
    async def get_file_url(self, name: str) -> URL:
        """Gets the URL of a file."""
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, file: File) -> URL:
        """Saves a file and returns its URL."""
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, url: URL) -> File:
        """Gets a file by its URL."""
        raise NotImplementedError


class DBSession(Protocol):
    """An interface for a database session."""

    @abstractmethod
    async def commit(self) -> None:
        """Commits the session."""
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        """Flushes the session."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class IdGenerator(Protocol):
    @abstractmethod
    def new_id(self) -> str:
        raise NotImplementedError
