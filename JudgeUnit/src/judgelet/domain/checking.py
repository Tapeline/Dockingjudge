from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import ClassVar, TYPE_CHECKING

from judgelet.domain.files import FileSystem
from judgelet.domain.results import Verdict, RunResult

if TYPE_CHECKING:
    from judgelet.domain.test_case import TestCase


class Validator[_ArgsT](ABC):
    """ABC for validators."""

    args_cls: type[_ArgsT]

    def __init__(self, args: _ArgsT) -> None:
        """Create validator with arguments."""
        self.args = args

    @abstractmethod
    def validate(
        self,
        result: RunResult,
        test_case: "TestCase",
        output_files: Mapping[str, str]
    ) -> Verdict:
        """Perform checking of the result."""
        raise NotImplementedError


class PrecompileChecker[_ArgsT](ABC):
    """ABC for precompile checks."""

    args_cls: type[_ArgsT]

    def __init__(self, args: _ArgsT) -> None:
        """Create precompile checker with arguments."""
        self.args = args

    @abstractmethod
    def check(self, filesystem: FileSystem, path: str) -> Verdict:
        """Perform checking of single file."""
        raise NotImplementedError


class NoArgs:
    """Dummy config class."""

    def __init__(self, *args, **kwargs) -> None:
        ...
