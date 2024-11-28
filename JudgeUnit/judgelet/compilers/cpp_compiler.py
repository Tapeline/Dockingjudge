"""
C++ language support
"""

from judgelet.compilers.abc_compiler import RunVerdict, UtilityRunResult
from judgelet.compilers.default_compiler import DefaultCompiler
from judgelet.sandbox.sandbox import Sandbox, SandboxResult


class CppCompiler(DefaultCompiler):
    """C++17 Compiler"""
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    file_ext = "cpp"

    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def compile(self, file_path: str, compile_timeout,
                      solution_dir) -> UtilityRunResult:
        sandbox = Sandbox(solution_dir)
        result = await sandbox.run(
            f"g++ -std=c++17 -O2 -o solution {file_path}",
            proc_input="",
            timeout_s=10,
            memory_limit_mb=512
        )
        sandbox.close()
        self._context["compiled"] = "solution"
        if result.return_code != 0:
            return UtilityRunResult.err(
                RunVerdict.CE,
                "stdout >>>>>\n" + result.stdout +
                "\n\nstderr >>>>>\n" + result.stderr
            )
        return UtilityRunResult.ok()

    async def test_impl(self, file_path: str, proc_input: str,
                        timeout: float, mem_limit_mb: float,
                        sandbox: Sandbox) -> SandboxResult:
        return await sandbox.run(
            f"./{self._context['compiled']}",
            proc_input=proc_input,
            timeout_s=timeout,
            memory_limit_mb=mem_limit_mb
        )
