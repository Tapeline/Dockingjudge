import os

IO_ENCODING = os.getenv("IO_ENCODING") or "utf-8"

# Precompile checkers
NO_IMPORT_PRECOMPILE_CHECKER_PATTERNS = {
    "py": ("import",),
}
