"""Does not contain regex pattern checker impl"""

import os.path
import re

from judgelet.exceptions import SerializationException
from judgelet.models import PrecompileCheckerModel
from judgelet.testing.precompile.abc_precompile_checker import AbstractPrecompileChecker


class PatternPrecompileChecker(AbstractPrecompileChecker):
    """Regex pattern checker impl"""

    def __init__(self, patterns: dict[str, list[str]], positive: bool):
        self._patterns = patterns
        self._is_positive = positive

    async def perform_check(self, solution_dir, files: list[str]) -> bool:
        return all(self._perform_check_on_file(solution_dir, file) for file in files)

    def _perform_check_on_file(self, solution_dir, file: str):
        """Check single file"""
        extension = os.path.basename(file).split(".")[-1]
        if extension not in self._patterns:
            return True
        patterns = self._patterns[extension]
        with open(os.path.join(solution_dir, file), "r") as f:
            data = f.read()
            for pattern in patterns:
                if re.search(pattern, data):
                    return self._is_positive
        return not self._is_positive


class NoPatternPrecompileChecker(PatternPrecompileChecker):
    # pylint: disable=missing-class-docstring
    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        if not isinstance(checker.parameters.get("patterns"), dict):
            raise SerializationException
        return NoPatternPrecompileChecker(checker.parameters["patterns"],
                                          positive=False)


class ContainsPatternPrecompileChecker(PatternPrecompileChecker):
    # pylint: disable=missing-class-docstring
    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        if not isinstance(checker.parameters.get("patterns"), dict):
            raise SerializationException
        return NoPatternPrecompileChecker(checker.parameters["patterns"],
                                          positive=True)
