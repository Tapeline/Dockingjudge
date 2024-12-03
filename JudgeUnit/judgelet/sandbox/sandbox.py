"""Provides tools for sandboxing processes"""

import enum
import shutil
from dataclasses import dataclass
from typing import Final

from judgelet import settings
from judgelet.sandbox import shell_executor

MEMORY_LIMIT_EXIT_CODE: Final[int] = 170
TIMEOUT_EXIT_CODE: Final[int] = 171


class SandboxExitCause(enum.Enum):
    """Reason why sandbox exited"""

    PROCESS_EXITED = enum.auto()
    MEMORY_LIMIT_EXCEEDED = enum.auto()
    TIME_LIMIT_EXCEEDED = enum.auto()


@dataclass(frozen=True)
class SandboxResult:
    """Result of running process in sandbox"""

    return_code: int
    cause: SandboxExitCause
    stdout: str | None = None
    stderr: str | None = None


class Sandbox:
    """Sandbox"""

    def __init__(
            self,
            sandbox_dir: str,
            encoding: str | None = settings.IO_ENCODING,
            environment: dict[str, str] | None = None
    ):
        """Create sandbox at directory"""
        self.sandbox_dir = sandbox_dir
        self.encoding = encoding
        self.environment = environment

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
        clean_command = cmd.replace('"', r'\"')
        result = await shell_executor.execute_in_shell(  # noqa: WPS110 (bad name)
            f'python -m llaunch {timeout_s} {memory_limit_mb} "{clean_command}"',
            proc_input=proc_input,
            cwd=self.sandbox_dir,
            io_encoding=self.encoding,
            env=self.environment
        )
        if result.return_code == MEMORY_LIMIT_EXIT_CODE:
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.MEMORY_LIMIT_EXCEEDED
            )
        if result.return_code == TIMEOUT_EXIT_CODE:
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.TIME_LIMIT_EXCEEDED
            )
        return SandboxResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.return_code,
            cause=SandboxExitCause.PROCESS_EXITED
        )

    def close(self):
        """Destroy the sandbox, but preserve files"""

    def destroy(self):
        """Destroy the sandbox and delete all files"""
        self.close()
        shutil.rmtree(self.sandbox_dir)
