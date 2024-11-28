"""
Python language support
"""

from judgelet.compilers.abc_compiler import UtilityRunResult
from judgelet.compilers.default_compiler import DefaultCompiler
from judgelet.sandbox.sandbox import Sandbox, SandboxResult


class PythonInterpreter(DefaultCompiler):
    """Python interpreter"""
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    file_ext = "py"

    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def compile(self, file_path: str, compile_timeout, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def test_impl(self, file_path: str, proc_input: str,
                        timeout: float, mem_limit_mb: float,
                        sandbox: Sandbox) -> SandboxResult:
        return await sandbox.run(
            f"python {file_path}",
            proc_input=proc_input,
            timeout_s=timeout,
            memory_limit_mb=mem_limit_mb
        )
