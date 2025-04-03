"""Does not contain regex pattern checker impl"""

import os
import re
from typing import override

from judgelet.exceptions import SerializationException
from judgelet.models import PrecompileCheckerModel
from judgelet.testing.precompile.abc_precompile_checker import \
    AbstractPrecompileChecker

# TODO: consider moving away from package with abstractions


class PatternPrecompileChecker(AbstractPrecompileChecker):
    """Regex pattern checker impl"""

    PATTERNS_ARG_FIELD = "patterns"

    def __init__(self, patterns: dict[str, list[str]], positive: bool):
        """
        Create regex pattern precompile checker
        Args:
            patterns: dict, where key is compiler name and value
                      is the list of all wanted patterns
            positive: if positive, enforces the file to have at least
                      one occurrence of one of aforementioned patterns.
                      if negative, enforces the file to not have any
                      defined pattern
        """
        self._patterns = patterns
        self._is_positive = positive

    @override
    async def perform_check(self, solution_dir, files: list[str]) -> bool:
        return all(
            self._perform_check_on_file(solution_dir, solution_file)
            for solution_file in files
        )

    def _perform_check_on_file(self, solution_dir, filename: str):
        """Check single file"""
        extension = os.path.basename(filename).split(".")[-1]
        if extension not in self._patterns:
            return True
        patterns = self._patterns[extension]
        with open(os.path.join(solution_dir, filename), "r") as target_file:
            file_contents = target_file.read()
            for pattern in patterns:
                if re.search(pattern, file_contents):
                    return self._is_positive
        return not self._is_positive


class NoPatternPrecompileChecker(PatternPrecompileChecker):
    """Enforce the code no not have some pattern"""

    @classmethod
    @override
    def deserialize(cls, checker: PrecompileCheckerModel):
        if not isinstance(checker.parameters.get(cls.PATTERNS_ARG_FIELD), dict):
            raise SerializationException
        return NoPatternPrecompileChecker(
            checker.parameters[cls.PATTERNS_ARG_FIELD],
            positive=False
        )


class ContainsPatternPrecompileChecker(PatternPrecompileChecker):
    """Enforce the code to have some pattern"""

    @classmethod
    @override
    def deserialize(cls, checker: PrecompileCheckerModel):
        if not isinstance(checker.parameters.get(cls.PATTERNS_ARG_FIELD), dict):
            raise SerializationException
        return NoPatternPrecompileChecker(
            checker.parameters[cls.PATTERNS_ARG_FIELD],
            positive=True
        )
