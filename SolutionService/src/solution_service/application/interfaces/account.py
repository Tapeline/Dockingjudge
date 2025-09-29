from abc import abstractmethod, ABC
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    settings: dict | None
    profile_pic: str | None
    roles: list[str]


class AbstractAccountService(ABC):
    @abstractmethod
    async def get_users_by_ids(self, ids: Sequence[int]) -> Sequence[UserDTO]:
        raise NotImplementedError
