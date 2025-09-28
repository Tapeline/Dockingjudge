from typing import override

from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import FileSystem
from judgelet.domain.results import RunResult
from judgelet.domain.sandbox import Sandbox
from judgelet.infrastructure.common import map_sandbox_cause_to_exit_state


class PythonCompiler(LanguageBackend):
    """Python language backend."""

    file_ext = "py"

    def __init__(self) -> None:
        self._target: str = ""

    @override
    async def prepare(
        self, fs: FileSystem, target_file: str, sandbox: Sandbox,
    ) -> RunResult:
        return RunResult.blank_ok()

    @override
    async def compile(
        self,
        fs: FileSystem,
        target_file: str,
        compile_timeout_s: float,
        sandbox: Sandbox,
    ) -> RunResult:
        self._target = target_file
        return RunResult.blank_ok()

    @override
    async def run(
        self,
        stdin: str,
        timeout_s: float,
        mem_limit_mb: float,
        sandbox: Sandbox,
    ) -> RunResult:
        sandbox_result = await sandbox.run(
            f"python {self._target}",
            proc_input=stdin,
            timeout_s=timeout_s,
            memory_limit_mb=mem_limit_mb,
        )
        exit_state = map_sandbox_cause_to_exit_state(sandbox_result.cause)
        return RunResult(
            sandbox_result.stdout or "",
            sandbox_result.stderr or "",
            sandbox_result.return_code,
            exit_state,
        )
