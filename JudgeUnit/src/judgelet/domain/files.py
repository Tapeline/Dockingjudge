"""Contains classes related to files and file system."""

from abc import ABC, abstractmethod
from collections.abc import Collection, Sequence, Mapping
from contextlib import contextmanager
from pathlib import Path

from attrs import frozen


@frozen
class File:
    """Represents a single file."""

    name: str
    contents: str


class Solution(ABC):
    """Represents a solution."""

    def __init__(self, uid: str) -> None:
        self.uid = uid

    @property
    @abstractmethod
    def files(self) -> Sequence[File]:
        """Get all files inside solution. Must be at least 1 file."""
        raise NotImplementedError

    @property
    @abstractmethod
    def main_file_name(self) -> str | None:
        """Get main file name. If none - first file is considered main."""
        raise NotImplementedError

    @property
    def main_file(self) -> File:
        filename = self.main_file_name
        if filename is None:
            return self.files[0]
        return next(file for file in self.files if file.name == filename)


class FileSystem(ABC):
    """File system abstraction."""

    @abstractmethod
    def place_solution(self, solution: Solution) -> Path:
        """Place all solution files."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self, solution: Solution) -> None:
        """Remove all solution files and cleanup root."""
        raise NotImplementedError

    @abstractmethod
    def get_file(self, path: str) -> File | None:
        """Get file by path."""
        raise NotImplementedError

    @abstractmethod
    def save_file(self, file: File) -> None:
        """Save file (overwrite if needed)."""
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        """Delete file by path."""
        raise NotImplementedError


class FileIO:
    def __init__(
            self,
            fs: FileSystem,
            input_files: Mapping[str, str],
            output_files: Collection[str]
    ):
        self.fs = fs
        self.input_files = input_files
        self.output_files = output_files
        self.output_files_data: Mapping[str, str] = {}

    def __enter__(self) -> None:
        for filename, contents in self.input_files.items():
            self.fs.save_file(File(filename, contents))

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        files = {}
        for filename in self.output_files:
            file = self.fs.get_file(filename)
            files[filename] = file.contents if file else None
            self.fs.delete_file(filename)
        self.output_files_data = files
        for filename in self.input_files.keys():
            self.fs.delete_file(filename)
