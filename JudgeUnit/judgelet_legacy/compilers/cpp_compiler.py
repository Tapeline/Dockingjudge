"""C++ language support"""
from typing import override

from judgelet.compilers.abc_compiler import RunVerdict, UtilityRunResult
from judgelet.compilers.default_compiler import DefaultCompiler
from judgelet.sandbox.sandbox import Sandbox, SandboxResult

# TODO: consider moving away from package with abstractions


class CppCompiler(DefaultCompiler):
    """C++17 Compiler"""

    COMPILE_TIME_LIMIT_S = 10
    COMPILE_MEMORY_LIMIT_MB = 512

    file_ext = "cpp"

    @override
    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    @override
    async def compile(
            self,
            file_path: str,
            compile_timeout: int,
            solution_dir: str,
    ) -> UtilityRunResult:
        sandbox = Sandbox(solution_dir)
        result = await sandbox.run(  # noqa: WPS110 (bad name)
            f"g++ -std=c++17 -O2 -o solution {file_path}",
            proc_input="",
            timeout_s=self.COMPILE_TIME_LIMIT_S,
            memory_limit_mb=self.COMPILE_MEMORY_LIMIT_MB
        )
        sandbox.close()
        self._context["compiled"] = "solution"
        if result.return_code != 0:
            return UtilityRunResult.err(
                RunVerdict.CE,
                f"stdout >>>>>\n{result.stdout}\n\nstderr >>>>>\n{result.stderr}"
            )
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
            f"./{self._context['compiled']}",
            proc_input=proc_input,
            timeout_s=timeout,
            memory_limit_mb=mem_limit_mb
        )
