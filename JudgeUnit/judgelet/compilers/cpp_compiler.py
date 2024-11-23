"""
C++ language support
"""
import asyncio

from judgelet.compilers import shell_executor
from judgelet.compilers.abc_compiler import AbstractCompiler, RunResult, RunVerdict, UtilityRunResult
from judgelet.settings import IO_ENCODING


class CppCompiler(AbstractCompiler):
    """C++17 Compiler"""
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    file_ext = "cpp"

    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def compile(self, file_path: str, compile_timeout,
                      solution_dir) -> UtilityRunResult:
        result = await shell_executor.execute_in_shell(
            f"g++ -std=c++17 -O2 -o solution {file_path}",
            timeout=10,
            cwd=solution_dir
        )
        self._context["compiled"] = "solution"
        if result.return_code != 0:
            return UtilityRunResult.err(
                RunVerdict.CE,
                b"stdout >>>>>\n" + result.stdout +
                b"\n\nstderr >>>>>\n" + result.stderr
            )
        return UtilityRunResult.ok()

    async def test(self, file_path: str, proc_input: str,
                   file_input: dict[str, str], required_back_files: set[str],
                   timeout: int, mem_limit_mb: int,
                   solution_dir) -> RunResult:
        try:
            result = await shell_executor.execute_in_shell(
                f"./{self._context['compiled']}",
                proc_input=proc_input,
                timeout=timeout,
                cwd=solution_dir
            )
            returning_files = self.load_files(required_back_files)
            if returning_files is None:
                return RunResult(
                    result.return_code,
                    result.stdout.decode(IO_ENCODING).replace('\r\n', '\n'),
                    result.stderr.decode(IO_ENCODING).replace('\r\n', '\n'),
                    RunVerdict.REQUIRED_FILE_NOT_FOUND,
                    {}
                )
            return RunResult(
                result.return_code,
                result.stdout.decode(IO_ENCODING).replace('\r\n', '\n'),
                result.stderr.decode(IO_ENCODING).replace('\r\n', '\n'),
                RunVerdict.OK,
                returning_files
            )
        except asyncio.exceptions.TimeoutError:
            return RunResult(-1, "", "", RunVerdict.TL, {})
