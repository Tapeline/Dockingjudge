import os
import re
from types import MappingProxyType
from typing import Final

from pydantic import BaseModel

from judgelet.application.constants import NO_IMPORT_PATTERNS
from judgelet.domain.checking import PrecompileChecker, NoArgs
from judgelet.domain.files import FileSystem
from judgelet.domain.results import Verdict


class _PatternCheckerArgs(BaseModel):
    patterns: dict[str, list[str]]


class HasPatternChecker(PrecompileChecker[_PatternCheckerArgs]):
    _args_cls = _PatternCheckerArgs

    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        checker = _RegexChecker(
            filesystem, self.args.patterns, is_positive=True
        )
        if checker.perform_check(path):
            return Verdict.OK()
        return Verdict.PCF(f"pattern check failed on {path}")


class NoPatternChecker(PrecompileChecker[_PatternCheckerArgs]):
    _args_cls = _PatternCheckerArgs

    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        checker = _RegexChecker(
            filesystem, self.args.patterns, is_positive=False
        )
        if checker.perform_check(path):
            return Verdict.OK()
        return Verdict.PCF(f"pattern check failed on {path}")


class NoImportChecker(PrecompileChecker[NoArgs]):
    _args_cls = NoArgs

    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        checker = _RegexChecker(
            filesystem, NO_IMPORT_PATTERNS, is_positive=True
        )
        if checker.perform_check(path):
            return Verdict.OK()
        return Verdict.PCF(f"pattern check failed on {path}")


class _RegexChecker:
    def __init__(
            self,
            fs: FileSystem,
            patterns: dict[str, list[str]],
            is_positive: bool
    ) -> None:
        """
        Create regex pattern precompile checker
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
        """Check single file"""
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

