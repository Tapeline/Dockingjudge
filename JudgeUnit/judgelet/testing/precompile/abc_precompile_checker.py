from abc import ABC, abstractmethod

from judgelet.exceptions import SerializationException
from judgelet.models import PrecompileCheckerModel


class AbstractPrecompileChecker(ABC):
    CHECKERS: dict[str, type["AbstractPrecompileChecker"]] = {}

    @abstractmethod
    async def perform_check(self, solution_dir, files: list[str]) -> bool:
        raise NotImplementedError

    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        if checker.type not in AbstractPrecompileChecker.CHECKERS:
            raise SerializationException("Precompile checker not found")
        cls = AbstractPrecompileChecker.CHECKERS[checker.type]
        return cls.deserialize(checker)


def register_default_precompile_checkers():
    from judgelet.testing.precompile.no_import_checker import NoImportPrecompileChecker
    from judgelet.testing.precompile.no_pattern_checker import NoPatternPrecompileChecker
    AbstractPrecompileChecker.CHECKERS["no_import"] = NoImportPrecompileChecker
    AbstractPrecompileChecker.CHECKERS["no_pattern"] = NoPatternPrecompileChecker
