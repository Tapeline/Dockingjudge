# pylint: disable=line-too-long

"""
Judgelet settings
"""

import os

IO_ENCODING = os.getenv("IO_ENCODING") or "utf-8"

NO_IMPORT_PRECOMPILE_CHECKER_PATTERNS = {
    "py": ("import",),
}

COMPILERS = {
    "python": "judgelet.compilers.python_compiler.PythonInterpreter"
}

PRECOMPILE_CHECKERS = {
    "no_import": "judgelet.testing.precompile.no_import_checker.NoImportPrecompileChecker",
    "no_pattern": "judgelet.testing.precompile.no_pattern_checker.NoPatternPrecompileChecker",
    "contains_pattern": "judgelet.testing.precompile.contains_pattern_checker.ContainsPatternPrecompileChecker",
}

VALIDATORS = {
    "stdout": "judgelet.testing.validators.stdout_validator.StdoutValidator",
    "file": "judgelet.testing.validators.file_validator.FileValidator"
}
