from types import MappingProxyType
from typing import Final

NO_IMPORT_PATTERNS: Final = MappingProxyType({
    "py": ("^import .*$", "^from .*? import .*$"),
})

