"""No-import checker impl"""

from judgelet import settings
from judgelet.models import PrecompileCheckerModel
from judgelet.testing.precompile.pattern_checker import NoPatternPrecompileChecker


class NoImportPrecompileChecker(NoPatternPrecompileChecker):
    """No-import checker impl"""
    def __init__(self):
        super().__init__(settings.NO_IMPORT_PRECOMPILE_CHECKER_PATTERNS,
                         positive=False)

    @staticmethod
    def deserialize(checker: PrecompileCheckerModel):
        return NoImportPrecompileChecker()
