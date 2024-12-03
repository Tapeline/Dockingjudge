"""Provides tools for encapsulating solution files"""

import base64
import io
import os
import zipfile
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import override

from judgelet.exceptions import SerializationException

StringPath = str


class File:  # noqa: WPS110 (wrong name)
    """Represents a file"""

    class ContentType(Enum):  # noqa: D106 (no doc)
        STRING = "str"
        BASE64 = "b64"

    def __init__(
            self,
            name: str,
            content: str,  # noqa: WPS110 (bad name)
            content_type: ContentType = ContentType.STRING
    ):
        """Create a virtual file"""
        self.name = name
        self.content = content  # noqa: WPS110 (bad name)
        self.content_type = content_type

    def place(self, base_path: StringPath) -> StringPath:
        """Deploy this file onto base_path"""
        self._ensure_path_exists(os.path.join(base_path, self.name))
        if self.content_type == File.ContentType.STRING:
            return self._place_string(base_path)
        if self.content_type == File.ContentType.BASE64:
            return self._place_b64(base_path)
        raise ValueError(f"Unresolved content type {self.content_type}")

    def _ensure_path_exists(self, path):
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    def _place_string(self, base_path: StringPath) -> StringPath:
        """Place file with string contents"""
        path = os.path.join(base_path, self.name)
        with open(path, "w") as target_file:
            target_file.write(self.content)
        return path

    def _place_b64(self, base_path: StringPath) -> StringPath:
        """Place file with base64 contents"""
        path = os.path.join(base_path, self.name)
        with open(path, "wb") as target_file:
            target_file.write(base64.b64decode(self.content))
        return path


class SolutionContainer(ABC):
    """Encapsulates solution files"""

    @abstractmethod
    def get_files(self) -> list[File]:
        """Get all container virtual files"""
        raise NotImplementedError

    @abstractmethod
    def get_main_file(self) -> StringPath:
        """Get file subjected for compilation and testing"""
        raise NotImplementedError

    @staticmethod
    def from_json(json_data: dict):
        """Deserialize"""
        # TODO: shouldn't pydantic be used here?
        if "type" not in json_data:
            raise SerializationException
        if json_data["type"] not in {"string", "zip"}:
            raise SerializationException
        return {
            "string": StringSolutionContainer,
            "zip": ZipSolutionContainer
        }[json_data["type"]].deserialize(json_data)


class StringSolutionContainer(SolutionContainer):
    """Single-file container"""

    def __init__(self, name: str, code: str):
        """Create container"""
        self._name = name
        self._code = code

    @override
    def get_files(self) -> list[File]:
        return [File(self._name, self._code, File.ContentType.STRING)]

    @override
    def get_main_file(self) -> StringPath:
        return self._name

    @staticmethod
    def deserialize(raw_data: dict) -> "StringSolutionContainer":
        """Deserialize"""
        if not isinstance(raw_data.get("name"), str):
            raise SerializationException
        if not isinstance(raw_data.get("code"), str):
            raise SerializationException
        return StringSolutionContainer(raw_data["name"], raw_data["code"])


class ZipSolutionContainer(SolutionContainer):
    """Solution container for base64-encoded ZIP"""

    def __init__(self, bin_data: bytes, main_file: str):
        """Create zip container from binary data"""
        self._bin = bin_data
        self._main_file = main_file
        self._files = []
        self._decompress()

    def _decompress(self):
        """Decompress virtually"""
        with io.BytesIO(self._bin) as b_io:
            zip_file = zipfile.ZipFile(b_io)
            for file in zip_file.namelist():  # noqa: WPS110 (bad name)
                with zip_file.open(file, "r") as zf_io:
                    self._files.append(File(
                        file,
                        base64.b64encode(zf_io.read()).decode(),
                        File.ContentType.BASE64
                    ))

    @override
    def get_files(self) -> list[File]:
        return self._files

    @override
    def get_main_file(self) -> StringPath:
        return self._main_file

    @staticmethod
    def deserialize(raw_data: dict) -> "ZipSolutionContainer":
        """Deserialize"""
        if not isinstance(raw_data.get("b64"), str):
            raise SerializationException
        if not isinstance(raw_data.get("main"), str):
            raise SerializationException
        return ZipSolutionContainer.from_b64(raw_data["b64"], raw_data["main"])

    @staticmethod
    def from_b64(zip_base64: str, main_file: str) -> "ZipSolutionContainer":
        """Decode zip from base64"""
        return ZipSolutionContainer(base64.b64decode(zip_base64), main_file)


def place_all_solution_files(solution: SolutionContainer, base_path: StringPath):
    """Place whole solution"""
    for solution_file in solution.get_files():
        solution_file.place(base_path)
