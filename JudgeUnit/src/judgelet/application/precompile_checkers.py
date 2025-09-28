import os
import re
from types import MappingProxyType
from typing import Final, override

from pydantic import BaseModel

from judgelet.application.constants import NO_IMPORT_PATTERNS
from judgelet.domain.checking import PrecompileChecker, NoArgs
from judgelet.domain.files import FileSystem
from judgelet.domain.results import Verdict


type LanguageName = str
type RegexPattern = str
type AssociatedLanguagePatterns = dict[LanguageName, list[RegexPattern]]


class _PatternCheckerArgs(BaseModel):
    patterns: dict[str, list[str]]


class HasPatternChecker(PrecompileChecker[_PatternCheckerArgs]):
    """Ensures that at least one pattern is present."""

    args_cls = _PatternCheckerArgs

    @override
    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        return _perform_pattern_check(
            filesystem, path, self.args.patterns, is_positive=True
        )


class NoPatternChecker(PrecompileChecker[_PatternCheckerArgs]):
    """Ensures that no pattern is present."""

    args_cls = _PatternCheckerArgs

    @override
    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        return _perform_pattern_check(
            filesystem, path, self.args.patterns, is_positive=False
        )


class NoImportChecker(PrecompileChecker[NoArgs]):
    """Ensures that no imports are present."""

    args_cls = NoArgs

    @override
    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        return _perform_pattern_check(
            filesystem, path, NO_IMPORT_PATTERNS, is_positive=False
        )


def _perform_pattern_check(
    filesystem: FileSystem,
    path: str,
    patterns: AssociatedLanguagePatterns,
    *,
    is_positive: bool,
) -> Verdict:
    checker = _RegexChecker(filesystem, patterns, is_positive=is_positive)
    if checker.perform_check(path):
        return Verdict.OK()
    return Verdict.PCF(f"pattern check failed on {path}")


class _RegexChecker:
    def __init__(
        self,
        fs: FileSystem,
        patterns: AssociatedLanguagePatterns,
        is_positive: bool
    ) -> None:
        """
        Create regex pattern precompile checker.

        Args:
            patterns: dict, where key is compiler name and value
                is the list of all wanted patterns
            is_positive: if positive, enforces the file to have at least
                one occurrence of one of aforementioned patterns.
                if negative, enforces the file to not have any
                defined pattern

        """
        self._patterns = patterns
        self._is_positive = is_positive
        self._fs = fs

    def perform_check(self, filename: str):
        """Check single file."""
        extension = os.path.basename(filename).split(".")[-1]
        if extension not in self._patterns:
            return True
        patterns = self._patterns[extension]
        target_file = self._fs.get_file(filename)
        for pattern in patterns:
            if re.search(pattern, target_file.contents):
                return self._is_positive
        return not self._is_positive


CHECKERS: Final = MappingProxyType({
    "has_pattern": HasPatternChecker,
    "no_pattern": NoPatternChecker,
    "no_import": NoImportChecker
})
