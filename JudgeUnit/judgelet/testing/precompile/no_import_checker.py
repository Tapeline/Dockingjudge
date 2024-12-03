"""No-import checker impl"""
from typing import override

from judgelet import settings
from judgelet.models import PrecompileCheckerModel
from judgelet.testing.precompile.pattern_checker import \
    NoPatternPrecompileChecker

# TODO: consider moving away from package with abstractions


class NoImportPrecompileChecker(NoPatternPrecompileChecker):
    """No-import checker impl"""

    def __init__(self):
        """Create no import checker with default settings specified"""
        super().__init__(
            settings.NO_IMPORT_PRECOMPILE_CHECKER_PATTERNS,
            positive=False
        )

    @staticmethod
    @override
    def deserialize(checker: PrecompileCheckerModel):
        return NoImportPrecompileChecker()
