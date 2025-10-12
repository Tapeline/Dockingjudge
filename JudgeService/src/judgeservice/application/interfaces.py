from abc import abstractmethod
from typing import Protocol


class SolutionGateway(Protocol):
    """Provides methods for getting solutions."""

    @abstractmethod
    async def get_solution_file(self, url: str) -> bytes:
        """Get solution dile by url."""
        raise NotImplementedError
