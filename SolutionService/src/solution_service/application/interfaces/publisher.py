from abc import ABC, abstractmethod

from dishka import FromDishka

from solution_service.application.interfaces.storage import AbstractStorage
from solution_service.domain.entities.abstract import CodeSolution


class AbstractSolutionPublisher(ABC):
    @abstractmethod
    async def publish(self, solution: CodeSolution, test_suite: dict) -> None:
        raise NotImplementedError
