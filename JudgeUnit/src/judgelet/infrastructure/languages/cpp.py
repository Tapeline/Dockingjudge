from typing import Final, override

from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import FileSystem
from judgelet.domain.results import ExitState, RunResult
from judgelet.domain.sandbox import Sandbox
from judgelet.infrastructure.common import map_sandbox_cause_to_exit_state

_COMPILE_MEMORY_LIMIT_MB: Final = 512


class Cpp17Compiler(LanguageBackend):
    """Python language backend."""

    file_ext = "cpp"

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
        result = await sandbox.run(
            f"g++ -std=c++17 -O2 -o solution {target_file}",
            proc_input="",
            timeout_s=compile_timeout_s,
            memory_limit_mb=_COMPILE_MEMORY_LIMIT_MB,
        )
        self._target = "./solution"
        if result.return_code != 0:
            report = (
                f"stdout >>>>>\n{result.stdout}\n\n"
                f"stderr >>>>>\n{result.stderr}"
            )
            return RunResult(
                stdout=report,
                stderr=report,
                return_code=result.return_code,
                state=ExitState.ERROR,
            )
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
            self._target,
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
