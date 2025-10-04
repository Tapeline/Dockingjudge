import base64

from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from solution_service.application.dto import NewCodeSolution, NewQuizSolution
from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.contest import (
    CodeTaskDTO,
    QuizTaskDTO,
)
from solution_service.domain.abstract import (
    QuizSolution, TaskType,
    CodeSolution,
)


class UserFactory(DataclassFactory[User]):
    __model__ = User


class QuizSolutionFactory(DataclassFactory[QuizSolution]):
    __model__ = QuizSolution
    task_type = lambda: TaskType.QUIZ


class CodeSolutionFactory(DataclassFactory[CodeSolution]):
    __model__ = CodeSolution
    task_type = lambda: TaskType.CODE


class NewCodeSolutionFactory(DataclassFactory[NewCodeSolution]):
    __model__ = NewCodeSolution


class CodeTaskFactory(ModelFactory[CodeTaskDTO]):
    __model__ = CodeTaskDTO


class NewQuizSolutionFactory(DataclassFactory[NewQuizSolution]):
    __model__ = NewQuizSolution


class QuizTaskFactory(ModelFactory[QuizTaskDTO]):
    __model__ = QuizTaskDTO


def to_base64(b_data: str) -> str:
    return base64.b64encode(b_data.encode()).decode()


def from_base64(b_data: str) -> str:
    return base64.b64decode(b_data.encode()).decode()
