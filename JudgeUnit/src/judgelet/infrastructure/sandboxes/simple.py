import shutil
import sys
import time
from pathlib import Path
from typing import Mapping, override

from structlog import get_logger

from judgelet.application.interfaces import SandboxFactory
from judgelet.domain.files import FileSystem
from judgelet.domain.sandbox import Sandbox, SandboxResult, SandboxExitCause
from judgelet.infrastructure import shell_executor
from judgelet.infrastructure.shell_executor import (
    MEMORY_LIMIT_EXIT_CODE,
    TIMEOUT_EXIT_CODE
)


class SimpleSandbox(Sandbox):
    """Simple sandbox that uses llaunch to control resources."""

    def __init__(
        self,
        fs: FileSystem,
        sandbox_dir: str,
        encoding: str | None = None,
        environment: Mapping[str, str] | None = None
    ):
        super().__init__(fs, sandbox_dir, encoding, environment)
        self.log = get_logger().bind(dir=sandbox_dir)

    async def run(
            self,
            cmd: str,
            proc_input: str,
            timeout_s: float,
            memory_limit_mb: float
    ) -> SandboxResult:
        clean_command = cmd.replace('"', r'\"')
        self.log.info("Copied llaunch")
        shutil.copy("llaunch.py", Path(self.sandbox_dir, "llaunch.py"))
        self.log.info(
            "Launching %s, M<=%s, T<=%s",
            clean_command, memory_limit_mb, timeout_s
        )
        start = time.time()
        result = await shell_executor.execute_in_shell(
            _get_command(timeout_s, memory_limit_mb, clean_command),
            proc_input=proc_input,
            cwd=self.sandbox_dir,
            io_encoding=self.encoding,
            env=self.environment
        )
        elapsed = time.time() - start
        if result.return_code == MEMORY_LIMIT_EXIT_CODE:
            self.log.info("Memory limit exceeded")
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.MEMORY_LIMIT_EXCEEDED
            )
        if result.return_code == TIMEOUT_EXIT_CODE:
            self.log.info(
                "Time limit exceeded",
                gross_error=elapsed - timeout_s
            )
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.TIME_LIMIT_EXCEEDED
            )
        self.log.info(
            "Launched and exited with return code %s", result.return_code
        )
        return SandboxResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.return_code,
            cause=SandboxExitCause.PROCESS_EXITED
        )

    @override
    def close(self):
        """Destroy the sandbox, but preserve temp files."""

    @override
    def destroy(self):
        """Destroy the sandbox and delete all temp files."""
        self.close()


def _get_command(time_limit: float, mem_limit: float, target: str) -> str:
    if sys.platform == "win32":
        return f'py -m llaunch {time_limit} {mem_limit} {target}'
    return f'python3 -m llaunch {time_limit} {mem_limit} "{target}"'


class SimpleSandboxFactory(SandboxFactory):
    @override
    def __call__(
            self,
            fs: FileSystem,
            sandbox_dir: str,
            encoding: str | None = None,
            environment: Mapping[str, str] | None = None
    ) -> Sandbox:
        return SimpleSandbox(fs, sandbox_dir, encoding, environment)
