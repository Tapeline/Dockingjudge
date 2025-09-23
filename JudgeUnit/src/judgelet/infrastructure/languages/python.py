from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import FileSystem
from judgelet.domain.results import RunResult, ExitState
from judgelet.domain.sandbox import Sandbox
from judgelet.infrastructure.common import map_sandbox_cause_to_exit_state


class PythonCompiler(LanguageBackend):
    def __init__(self) -> None:
        self._target: str = ""

    @property
    def file_ext(self) -> str:
        return "py"

    async def prepare(
            self, fs: FileSystem, target_file: str
    ) -> RunResult:
        return RunResult.blank_ok()

    async def compile(
            self, fs: FileSystem, target_file: str, compile_timeout_s: float
    ) -> RunResult:
        self._target = target_file
        return RunResult.blank_ok()

    async def run(
            self,
            stdin: str,
            timeout_s: float,
            mem_limit_mb: float,
            sandbox: Sandbox
    ) -> RunResult:
        sandbox_result = await sandbox.run(
            f"python {self._target}",
            proc_input=stdin,
            timeout_s=timeout_s,
            memory_limit_mb=mem_limit_mb
        )
        exit_state = map_sandbox_cause_to_exit_state(sandbox_result.cause)
        return RunResult(
            sandbox_result.stdout,
            sandbox_result.stderr,
            sandbox_result.return_code,
            exit_state
        )
