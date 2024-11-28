import enum
import shutil
from dataclasses import dataclass
from enum import Enum
from typing import Final

from judgelet.sandbox import shell_executor


MEMORY_LIMIT_EXIT_CODE: Final[int] = 170
TIMEOUT_EXIT_CODE: Final[int] = 171


class SandboxExitCause(Enum):
    PROCESS_EXITED = enum.auto()
    MEMORY_LIMIT_EXCEEDED = enum.auto()
    TIME_LIMIT_EXCEEDED = enum.auto()


@dataclass(frozen=True)
class SandboxResult:
    return_code: int
    cause: SandboxExitCause
    stdout: str | None = None
    stderr: str | None = None


class Sandbox:
    def __init__(
            self,
            sandbox_dir: str,
            encoding: str | None = None,
            environment: dict[str, str] | None = None
    ):
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
        result = await shell_executor.execute_in_shell(
            f"python -m llaunch {timeout_s} {memory_limit_mb} \"{cmd.replace('"', '\\"')}\"",
            proc_input=proc_input,
            cwd=self.sandbox_dir,
            io_encoding=self.encoding,
            env=self.environment
        )
        if result.return_code == MEMORY_LIMIT_EXIT_CODE:
            return SandboxResult(return_code=result.return_code,
                                 cause=SandboxExitCause.MEMORY_LIMIT_EXCEEDED)
        if result.return_code == TIMEOUT_EXIT_CODE:
            return SandboxResult(return_code=result.return_code,
                                 cause=SandboxExitCause.TIME_LIMIT_EXCEEDED)
        return SandboxResult(stdout=result.stdout, stderr=result.stderr,
                             return_code=result.return_code,
                             cause=SandboxExitCause.PROCESS_EXITED)

    def close(self):
        """Destroy the sandbox, but preserve files"""

    def destroy(self):
        """Destroy the sandbox and delete all files"""
        self.close()
        shutil.rmtree(self.sandbox_dir)
