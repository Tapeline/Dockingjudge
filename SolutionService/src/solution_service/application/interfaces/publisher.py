from abc import abstractmethod
from typing import Any, Protocol

from solution_service.domain.abstract import CodeSolution


class SolutionPublisher(Protocol):
    """Handles asynchronous messaging."""

    @abstractmethod
    async def publish(
        self,
        solution: CodeSolution,
        test_suite: dict[str, Any],
    ) -> None:
        """Publish solution to the message queue."""
        raise NotImplementedError
