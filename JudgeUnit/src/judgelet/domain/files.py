"""Contains classes related to files and file system."""

from abc import ABC, abstractmethod
from collections.abc import Collection, Mapping, Sequence
from pathlib import Path
from typing import Any

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
        """
        Get main file.

        If main_file_name is specified, then use it,
        otherwise use first file in collection.

        """
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
        """
        Delete file by path.

        If file does not exist, do not throw an error.

        """
        raise NotImplementedError


class FileIO:
    """Context manager to safely handle file IO within solution test."""

    def __init__(
        self,
        fs: FileSystem,
        input_files: Mapping[str, str],
        output_files: Collection[str],
    ) -> None:
        self.fs = fs
        self.input_files = input_files
        self.output_files = output_files
        self.output_files_data: Mapping[str, str] = {}

    def __enter__(self) -> None:
        """Place input files into solution dir."""
        for filename, contents in self.input_files.items():
            self.fs.save_file(File(filename, contents))

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: Any,
    ) -> None:
        """Load required answer files from solution dir."""
        files = {}
        for filename in self.output_files:
            file = self.fs.get_file(filename)
            files[filename] = file.contents if file else ""
            self.fs.delete_file(filename)
        self.output_files_data = files
        for filename in self.input_files:
            self.fs.delete_file(filename)
