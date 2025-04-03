"""Python language support"""
from typing import override

from judgelet.compilers.abc_compiler import UtilityRunResult
from judgelet.compilers.default_compiler import DefaultCompiler
from judgelet.sandbox.sandbox import Sandbox, SandboxResult

# TODO: consider moving away from package with abstractions


class PythonInterpreter(DefaultCompiler):
    """Python interpreter"""

    file_ext = "py"

    @override
    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    @override
    async def compile(self, file_path: str, compile_timeout, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    @override
    async def test_impl(  # noqa: WPS211 (too many args)
            self,
            file_path: str,
            proc_input: str,
            timeout: float,
            mem_limit_mb: float,
            sandbox: Sandbox
    ) -> SandboxResult:
        return await sandbox.run(
            f"python {file_path}",
            proc_input=proc_input,
            timeout_s=timeout,
            memory_limit_mb=mem_limit_mb
        )
