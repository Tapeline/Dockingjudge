from types import MappingProxyType
from typing import Final

from judgelet.infrastructure.languages.cpp import Cpp17Compiler
from judgelet.infrastructure.languages.python import PythonCompiler

LANGUAGES: Final = MappingProxyType({
    "python": PythonCompiler,
    "cpp17": Cpp17Compiler,
})

DEFAULT_FILENAMES: Final = MappingProxyType({
    "python": "main.py",
    "cpp17": "main.cpp"
})
