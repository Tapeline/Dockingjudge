import enum
from abc import ABC, abstractmethod
from typing import Final, Mapping

from attrs import frozen

from judgelet.domain.files import FileSystem


class SandboxExitCause(enum.Enum):
    """Reason why the sandbox has exited."""

    PROCESS_EXITED = enum.auto()
    MEMORY_LIMIT_EXCEEDED = enum.auto()
    TIME_LIMIT_EXCEEDED = enum.auto()


@frozen
class SandboxResult:
    """Result of running a process in the sandbox."""

    return_code: int
    cause: SandboxExitCause
    stdout: str | None = None
    stderr: str | None = None


class Sandbox(ABC):
    """Base sandbox class."""

    def __init__(
        self,
        fs: FileSystem,
        sandbox_dir: str,
        encoding: str | None = None,
        environment: Mapping[str, str] | None = None
    ):
        """Create sandbox at directory."""
        self.sandbox_dir = sandbox_dir
        self.encoding = encoding
        self.environment = environment
        self.fs = fs

    @abstractmethod
    async def run(
        self,
        cmd: str,
        proc_input: str,
        timeout_s: float,
        memory_limit_mb: float
    ) -> SandboxResult:
        """
        Run command in sandbox

        Args:
            cmd: target command
            proc_input: process stdin
            timeout_s: when to interrupt process with TL
            memory_limit_mb: when to interrupt process with ML

        Returns:
            Result of running the command

        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """Destroy the sandbox, but preserve temp files."""

    @abstractmethod
    def destroy(self):
        """Destroy the sandbox and delete all temp files."""
