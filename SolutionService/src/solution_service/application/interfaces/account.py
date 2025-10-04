from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, Any


@dataclass
class User:
    """Resembles a user."""

    id: int
    username: str
    settings: dict[str, Any] | None
    profile_pic: str | None
    roles: list[str]


class AccountService(Protocol):
    """Provides methods to work with accounts."""

    @abstractmethod
    async def get_users_by_ids(self, ids: Sequence[int]) -> Sequence[User]:
        """
        Get list of users by a list of ids.

        Users' ordering will be kept in accordance with ordering of ids.

        """
        raise NotImplementedError
