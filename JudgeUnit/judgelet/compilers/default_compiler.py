import os.path
from abc import ABC, abstractmethod
from pathlib import Path

from judgelet.compilers.abc_compiler import AbstractCompiler, RunResult, RunVerdict
from judgelet.sandbox.sandbox import Sandbox, SandboxExitCause, SandboxResult
from judgelet.settings import IO_ENCODING


class DefaultCompiler(AbstractCompiler, ABC):
    def _place_input_files(self, file_input: dict[str, str], sandbox: Sandbox):
        for filename, contents in file_input.items():
            filename = os.path.join(sandbox.sandbox_dir, filename)
            Path(filename).mkdir(parents=True, exist_ok=True)
            with open(filename, "w") as f:
                f.write(contents)

    def _create_sandbox(self, solution_dir, file_path: str,
                        file_input: dict[str, str], **kwargs) -> Sandbox:
        sandbox = Sandbox(solution_dir, **kwargs)
        self._place_input_files(file_input, sandbox)
        return sandbox

    async def test(self, file_path: str, proc_input: str,
                   file_input: dict[str, str], required_back_files: set[str],
                   timeout: float, mem_limit_mb: float, solution_dir) -> RunResult:
        sandbox = self._create_sandbox(solution_dir, file_path, file_input,
                                       encoding=IO_ENCODING)
        result = await self.test_impl(file_path, proc_input, timeout, mem_limit_mb, sandbox)

        if result.cause == SandboxExitCause.MEMORY_LIMIT_EXCEEDED:
            sandbox.close()
            return RunResult(result.return_code, "", "", RunVerdict.ML, {})
        if result.cause == SandboxExitCause.TIME_LIMIT_EXCEEDED:
            sandbox.close()
            return RunResult(result.return_code, "", "", RunVerdict.TL, {})

        returning_files = self.load_files(required_back_files)
        if returning_files is None:
            sandbox.close()
            return RunResult(result.return_code, "", "", RunVerdict.REQUIRED_FILE_NOT_FOUND, {})

        sandbox.close()
        return RunResult(
            result.return_code,
            (result.stdout or "").replace('\r\n', '\n'),
            (result.stderr or "").replace('\r\n', '\n'),
            RunVerdict.OK,
            returning_files
        )

    @abstractmethod
    async def test_impl(self, file_path: str, proc_input: str,
                        timeout: float, mem_limit_mb: float,
                        sandbox: Sandbox) -> SandboxResult:
        raise NotImplementedError
