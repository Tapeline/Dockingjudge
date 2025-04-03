"""Default abstract compiler"""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

from judgelet.compilers.abc_compiler import (AbstractCompiler, RunResult,
                                             RunVerdict)
from judgelet.sandbox.sandbox import Sandbox, SandboxExitCause, SandboxResult
from judgelet.settings import IO_ENCODING


class DefaultCompiler(AbstractCompiler, ABC):
    """Default abstract compiler"""

    @override
    async def run_solution(  # noqa: WPS211 (too many args)
            self,
            file_path: str,
            proc_input: str,
            file_input: dict[str, str],
            required_back_files: set[str],
            timeout: float,
            mem_limit_mb: float,
            solution_dir: str
    ) -> RunResult:
        sandbox = self._create_sandbox(
            solution_dir,
            file_input,
            encoding=IO_ENCODING
        )
        run_result = await self.test_impl(file_path, proc_input, timeout, mem_limit_mb, sandbox)

        if run_result.cause == SandboxExitCause.MEMORY_LIMIT_EXCEEDED:
            sandbox.close()
            return RunResult(run_result.return_code, "", "", RunVerdict.ML, {})
        if run_result.cause == SandboxExitCause.TIME_LIMIT_EXCEEDED:
            sandbox.close()
            return RunResult(run_result.return_code, "", "", RunVerdict.TL, {})

        returning_files = self.load_files(required_back_files)
        if returning_files is None:
            sandbox.close()
            return RunResult(run_result.return_code, "", "", RunVerdict.REQUIRED_FILE_NOT_FOUND, {})

        sandbox.close()
        return RunResult(
            run_result.return_code,
            (run_result.stdout or "").replace("\r\n", "\n"),
            (run_result.stderr or "").replace("\r\n", "\n"),
            RunVerdict.OK,
            returning_files
        )

    def _create_sandbox(
            self,
            solution_dir,
            file_input: dict[str, str],
            **kwargs
    ) -> Sandbox:
        sandbox = Sandbox(solution_dir, **kwargs)
        self._place_input_files(file_input, sandbox)
        return sandbox

    def _place_input_files(self, file_input: dict[str, str], sandbox: Sandbox):
        for filename, file_content in file_input.items():
            filename = os.path.join(sandbox.sandbox_dir, filename)
            Path(filename).mkdir(parents=True, exist_ok=True)
            with open(filename, "w") as file_handle:
                file_handle.write(file_content)

    @abstractmethod
    async def test_impl(  # noqa: WPS211 (too many args)
            self,
            file_path: str,
            proc_input: str,
            timeout: float,
            mem_limit_mb: float,
            sandbox: Sandbox
    ) -> SandboxResult:
        """Actual implementation of running code"""
        raise NotImplementedError
