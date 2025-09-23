from types import MappingProxyType
from typing import Final

from judgelet.infrastructure.languages.python import PythonCompiler

LANGUAGES: Final = MappingProxyType({
    "python": PythonCompiler
})

DEFAULT_FILENAMES: Final = MappingProxyType({
    "python": "main.py"
})
