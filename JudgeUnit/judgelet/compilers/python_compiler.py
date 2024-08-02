import asyncio
import subprocess

from judgelet.compilers.abc_compiler import Compiler, RunResult, RunVerdict, UtilityRunResult
from judgelet.settings import IO_ENCODING


class PythonInterpreter(Compiler):
    file_ext = "py"

    async def prepare(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str]) -> UtilityRunResult:
        self.save_files(file_input)
        return UtilityRunResult.ok()

    async def compile(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str]) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def test(self, file_path: str, proc_input: str,
                   file_input: dict[str, str], required_back_files: set[str],
                   timeout: int, mem_limit_mb: int) -> RunResult:
        try:
            process = subprocess.run(["python", file_path], input=proc_input.encode(IO_ENCODING),
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            # proc = await asyncio.create_subprocess_shell(
            #     f"python {file_path}",
            #     stdout=asyncio.subprocess.PIPE,
            #     stderr=asyncio.subprocess.PIPE
            # )
            # stdout, stderr = await asyncio.wait_for(
            #     proc.communicate(proc_input.encode(IO_ENCODING)),
            #     timeout=timeout
            # )
            returning_files = self.load_files(required_back_files)
            if returning_files is None:
                return RunResult(
                    process.returncode,
                    process.stdout.decode(IO_ENCODING).replace('\r\n', '\n'),
                    process.stderr.decode(IO_ENCODING).replace('\r\n', '\n'),
                    RunVerdict.REQUIRED_FILE_NOT_FOUND,
                    {}
                )
            return RunResult(
                process.returncode,
                process.stdout.decode(IO_ENCODING).replace('\r\n', '\n'),
                process.stderr.decode(IO_ENCODING).replace('\r\n', '\n'),
                RunVerdict.OK,
                returning_files
            )
        except subprocess.TimeoutExpired:
        #except asyncio.exceptions.TimeoutError:
            return RunResult(-1, "", "", RunVerdict.TL, {})
