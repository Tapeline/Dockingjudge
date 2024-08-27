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
    class ContentType(Enum):
        STRING = "str"
        BASE64 = "b64"

    def __init__(self, name, content,
                 content_type: ContentType = ContentType.STRING):
        self.name = name
        self.content = content
        self.content_type = content_type

    def place(self, base_path: StringPath) -> StringPath:
        self._ensure_path_exists(os.path.join(base_path, self.name))
        if self.content_type == File.ContentType.STRING:
            return self._place_string(base_path)
        elif self.content_type == File.ContentType.BASE64:
            return self._place_b64(base_path)

    def _ensure_path_exists(self, path):
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    def _place_string(self, base_path: StringPath) -> StringPath:
        with open(path := os.path.join(base_path, self.name), "w") as f:
            f.write(self.content)
        return path

    def _place_b64(self, base_path: StringPath) -> StringPath:
        with open(path := os.path.join(base_path, self.name), "wb") as f:
            f.write(base64.b64decode(self.content))
        return path


class SolutionContainer(ABC):
    @abstractmethod
    def get_files(self) -> list[File]:
        raise NotImplementedError

    @staticmethod
    def from_json(data):
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
        raise NotImplementedError


class StringSolutionContainer(SolutionContainer):
    def __init__(self, name: str, code: str):
        self._name = name
        self._code = code

    def get_files(self) -> list[File]:
        return [File(self._name, self._code, File.ContentType.STRING)]

    @staticmethod
    def deserialize(data) -> "StringSolutionContainer":
        if (
                not isinstance(data.get("name"), str) or
                not isinstance(data.get("code"), str)
        ):
            raise SerializationException
        return StringSolutionContainer(data["name"], data["code"])

    def get_main_file(self) -> StringPath:
        return self._name


class ZipSolutionContainer(SolutionContainer):
    @staticmethod
    def from_b64(zip_base64: str, main_file: str) -> "ZipSolutionContainer":
        return ZipSolutionContainer(base64.decode(zip_base64), main_file)

    def __init__(self, bin_data: bytes, main_file: str):
        self._bin = bin_data
        self._main_file = main_file
        self._files = []
        self._decompress()

    def _decompress(self):
        _io = io.BytesIO(self._bin)
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
        if not isinstance(data.get("b64"), str):
            raise SerializationException
        if not isinstance(data.get("main"), str):
            raise SerializationException
        return ZipSolutionContainer.from_b64(data["b64"], data["main"])


def place_all_solution_files(solution: SolutionContainer, base_path: StringPath):
    for file in solution.get_files():
        file.place(base_path)
