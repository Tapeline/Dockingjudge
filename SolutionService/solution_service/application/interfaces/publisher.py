from abc import ABC, abstractmethod

from solution_service.domain.entities.abstract import CodeSolution


class AbstractSolutionPublisher(ABC):
    @abstractmethod
    def publish(self, solution: CodeSolution) -> None:
        raise NotImplementedError
