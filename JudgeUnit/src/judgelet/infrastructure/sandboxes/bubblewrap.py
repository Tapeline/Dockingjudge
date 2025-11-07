import os
import shutil
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import override

from structlog import get_logger

from judgelet.application.interfaces import SandboxFactory
from judgelet.domain.files import FileSystem
from judgelet.domain.sandbox import Sandbox, SandboxExitCause, SandboxResult
from judgelet.infrastructure import shell_executor


class BubblewrapSandbox(Sandbox):
    """Simple sandbox that uses llaunch to control resources."""

    def __init__(
        self,
        fs: FileSystem,
        sandbox_dir: str,
        encoding: str | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(fs, sandbox_dir, encoding, environment)
        self.log = get_logger().bind(dir=sandbox_dir)

    @override
    async def run(
        self,
        cmd: str,
        proc_input: str,
        timeout_s: float,
        memory_limit_mb: float,
    ) -> SandboxResult:
        clean_command = cmd.replace('"', r'\"')
        self.log.info("Copied llaunch")
        shutil.copy("llaunch.py", Path(self.sandbox_dir, "llaunch.py"))
        self.log.info(
            "Launching %s, M<=%s, T<=%s",
            clean_command, memory_limit_mb, timeout_s,
        )
        final_cmd = _get_command(
            sys.platform, timeout_s, memory_limit_mb, clean_command,
            self.sandbox_dir,
        )
        self.log.info("Final cmd: %s", final_cmd)
        start = time.time()
        result = await shell_executor.execute_in_shell(
            final_cmd,
            proc_input=proc_input,
            cwd=self.sandbox_dir,
            io_encoding=self.encoding,
            env=self.environment,
        )
        elapsed = time.time() - start
        if result.return_code == shell_executor.MEMORY_LIMIT_EXIT_CODE:
            self.log.info("Memory limit exceeded")
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.MEMORY_LIMIT_EXCEEDED,
            )
        if result.return_code == shell_executor.TIMEOUT_EXIT_CODE:
            self.log.info(
                "Time limit exceeded",
                gross_error=elapsed - timeout_s,
            )
            return SandboxResult(
                return_code=result.return_code,
                cause=SandboxExitCause.TIME_LIMIT_EXCEEDED,
            )
        self.log.info(
            "Launched and exited with return code %s", result.return_code,
        )
        return SandboxResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.return_code,
            cause=SandboxExitCause.PROCESS_EXITED,
        )

    @override
    def close(self) -> None:
        """Destroy the sandbox, but preserve temp files."""

    @override
    def destroy(self) -> None:
        """Destroy the sandbox and delete all temp files."""
        self.close()


def _get_command(
    platform: str,
    time_limit: float,
    mem_limit: float,
    target: str,
    sandbox_dir: str,
) -> str:
    py_cmd = _get_py_command(platform, time_limit, mem_limit, target)
    if platform == "win32":
        return py_cmd
    sandbox_dir = os.path.abspath(sandbox_dir)
    return (
        f"bwrap "
        f"--ro-bind /usr /usr "
        f"--ro-bind /lib /lib "
        f"--ro-bind /app/llaunch.py llaunch.py "
        f"--ro-bind /bin/sh /bin/sh "
        f"--bind {sandbox_dir} {sandbox_dir} "
        f"--proc /proc "
        f"--dev /dev "
        f"--unshare-pid "
        f"--new-session "
        f"-- {py_cmd}"
    )


def _get_py_command(
    platform: str,
    time_limit: float,
    mem_limit: float,
    target: str,
) -> str:
    if platform == "win32":
        return f"py -m llaunch {time_limit} {mem_limit} {target}"
    return f'python3 -m llaunch {time_limit} {mem_limit} "{target}"'


class BubblewrapSandboxFactory(SandboxFactory):
    """Simple sandbox factory."""

    @override
    def __call__(
        self,
        fs: FileSystem,
        sandbox_dir: str,
        encoding: str | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> Sandbox:
        return BubblewrapSandbox(fs, sandbox_dir, encoding, environment)
