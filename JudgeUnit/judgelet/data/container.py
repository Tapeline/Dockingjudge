"""
Provides tools for encapsulating solution files
"""

import base64
import io
import os.path
import zipfile
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from judgelet.exceptions import SerializationException

StringPath = str


class File:
    """Represents a file"""
    # pylint: disable=too-few-public-methods
    class ContentType(Enum):
        # pylint: disable=missing-class-docstring
        STRING = "str"
        BASE64 = "b64"

    def __init__(self, name, content,
                 content_type: ContentType = ContentType.STRING):
        self.name = name
        self.content = content
        self.content_type = content_type

    def place(self, base_path: StringPath) -> StringPath:
        """Deploy this file"""
        self._ensure_path_exists(os.path.join(base_path, self.name))
        if self.content_type == File.ContentType.STRING:
            return self._place_string(base_path)
        if self.content_type == File.ContentType.BASE64:
            return self._place_b64(base_path)
        raise ValueError(f"Unresolved content type {self.content_type}")

    def _ensure_path_exists(self, path):
        # pylint: disable=missing-function-docstring
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    def _place_string(self, base_path: StringPath) -> StringPath:
        # pylint: disable=missing-function-docstring
        with open(path := os.path.join(base_path, self.name), "w") as f:
            f.write(self.content)
        return path

    def _place_b64(self, base_path: StringPath) -> StringPath:
        # pylint: disable=missing-function-docstring
        with open(path := os.path.join(base_path, self.name), "wb") as f:
            f.write(base64.b64decode(self.content))
        return path


class SolutionContainer(ABC):
    """Encapsulates solution files"""
    @abstractmethod
    def get_files(self) -> list[File]:
        """Get all files"""
        raise NotImplementedError

    @staticmethod
    def from_json(data):
        """Deserialize"""
        if "type" not in data:
            raise SerializationException
        if data["type"] not in ("string", "zip"):
            raise SerializationException
        return {
            "string": StringSolutionContainer,
            "zip": ZipSolutionContainer
        }[data["type"]].deserialize(data)

    @abstractmethod
    def get_main_file(self) -> StringPath:
        # pylint: disable=missing-function-docstring
        raise NotImplementedError


class StringSolutionContainer(SolutionContainer):
    """Single-file container"""
    def __init__(self, name: str, code: str):
        self._name = name
        self._code = code

    def get_files(self) -> list[File]:
        return [File(self._name, self._code, File.ContentType.STRING)]

    @staticmethod
    def deserialize(data) -> "StringSolutionContainer":
        # pylint: disable=missing-function-docstring
        if (
                not isinstance(data.get("name"), str) or
                not isinstance(data.get("code"), str)
        ):
            raise SerializationException
        return StringSolutionContainer(data["name"], data["code"])

    def get_main_file(self) -> StringPath:
        return self._name


class ZipSolutionContainer(SolutionContainer):
    """Solution container for base64-encoded ZIP"""
    @staticmethod
    def from_b64(zip_base64: str, main_file: str) -> "ZipSolutionContainer":
        """Decode zip from base64"""
        return ZipSolutionContainer(base64.b64decode(zip_base64), main_file)

    def __init__(self, bin_data: bytes, main_file: str):
        self._bin = bin_data
        self._main_file = main_file
        self._files = []
        self._decompress()

    def _decompress(self):
        # pylint: disable=missing-function-docstring
        with io.BytesIO(self._bin) as _io:
            z = zipfile.ZipFile(_io)
            for file in z.namelist():
                with z.open(file, "r") as f:
                    self._files.append(File(
                        file, base64.b64encode(f.read()), File.ContentType.BASE64
                    ))

    def get_main_file(self) -> StringPath:
        return self._main_file

    def get_files(self) -> list[File]:
        return self._files

    @staticmethod
    def deserialize(data) -> "ZipSolutionContainer":
        # pylint: disable=missing-function-docstring
        if not isinstance(data.get("b64"), str):
            raise SerializationException
        if not isinstance(data.get("main"), str):
            raise SerializationException
        return ZipSolutionContainer.from_b64(data["b64"], data["main"])


def place_all_solution_files(solution: SolutionContainer, base_path: StringPath):
    # pylint: disable=missing-function-docstring
    for file in solution.get_files():
        file.place(base_path)
