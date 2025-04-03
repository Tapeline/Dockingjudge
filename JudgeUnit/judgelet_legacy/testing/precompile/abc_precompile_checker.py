"""Abstractions for precompile checks"""

from abc import ABC, abstractmethod

from judgelet import settings
from judgelet.class_loader import load_class
from judgelet.exceptions import SerializationException
from judgelet.models import PrecompileCheckerModel


class AbstractPrecompileChecker(ABC):
    """ABC for precompile checkers"""

    CHECKERS: dict[str, type["AbstractPrecompileChecker"]] = {}

    @abstractmethod
    async def perform_check(self, solution_dir, files: list[str]) -> bool:
        """Validate solution before running"""
        raise NotImplementedError

    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        """Create checker from pydantic"""
        if checker.type not in AbstractPrecompileChecker.CHECKERS:
            raise SerializationException("Precompile checker not found")
        validator_class = AbstractPrecompileChecker.CHECKERS[checker.type]
        return validator_class.deserialize(checker)


def register_default_precompile_checkers():
    """Dependency injection mechanism"""
    for checker_name, checker_module in settings.PRECOMPILE_CHECKERS.items():
        AbstractPrecompileChecker.CHECKERS[checker_name] = load_class(
            checker_module, AbstractPrecompileChecker
        )
