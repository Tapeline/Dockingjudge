from abc import abstractmethod
from typing import Protocol

from solution_service.application.interfaces.account import User


class UserIdProvider(Protocol):
    """Provides user identity."""

    @abstractmethod
    async def get_user(self) -> User | None:
        """Get authenticated user or return none."""
        raise NotImplementedError

    @abstractmethod
    async def require_user(self) -> User:
        """Get authenticated user or raise error."""
        raise NotImplementedError
