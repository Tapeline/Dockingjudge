from abc import abstractmethod
from typing import Protocol

from judgeservice.domain.entities import Judgelet


class JudgeletPool(Protocol):
    """A pool of judgelets."""

    @abstractmethod
    async def get_for_compiler(self, compiler_name: str) -> Judgelet:
        """
        Get a single most suitable judgelet that supports given compiler.

        Args:
            compiler_name: compiler filter

        """
        raise NotImplementedError


class SolutionGateway(Protocol):
    """Provides methods for getting solutions."""

    @abstractmethod
    async def get_solution_file(self, url: str) -> bytes:
        """Get solution dile by url."""
        raise NotImplementedError
