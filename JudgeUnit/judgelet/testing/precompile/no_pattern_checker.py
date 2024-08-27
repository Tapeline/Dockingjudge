import os.path
import re

from judgelet import settings
from judgelet.exceptions import SerializationException
from judgelet.models import PrecompileCheckerModel
from judgelet.testing.precompile.abc_precompile_checker import AbstractPrecompileChecker


class NoPatternPrecompileChecker(AbstractPrecompileChecker):
    def __init__(self, patterns: dict[str, list[str]]):
        self._patterns = patterns

    async def perform_check(self, solution_dir, files: list[str]) -> bool:
        return all(self._perform_check_on_file(solution_dir, file) for file in files)

    def _perform_check_on_file(self, solution_dir, file: str):
        extension = os.path.basename(file).split(".")[-1]
        if extension not in self._patterns:
            return True
        patterns = self._patterns[extension]
        with open(os.path.join(solution_dir, file), "r") as f:
            data = f.read()
            for pattern in patterns:
                if re.search(pattern, data):
                    return False
        return True

    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        if not isinstance(checker.parameters.get("patterns"), dict):
            raise SerializationException
        return NoPatternPrecompileChecker(checker.parameters["patterns"])
