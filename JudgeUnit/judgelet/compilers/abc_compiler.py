"""
Abstractions for compilers
"""
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-positional-arguments

import os
from abc import abstractmethod, ABC
from enum import Enum

from judgelet import settings
from judgelet.class_loader import load_class


class RunVerdict(Enum):
    """Compiler verdict. OK even if wrong answer"""
    OK = "OK"
    TL = "TL"
    REQUIRED_FILE_NOT_FOUND = "FNF"
    ML = "ML"
    CE = "CE"  # Compilation error
    PF = "PF"  # Pre-check fail

    def to_string(self):
        """Get string representation"""
        if self == RunVerdict.REQUIRED_FILE_NOT_FOUND:
            return "PE"
        return self.value


class UtilityRunResult:
    """Run result returned by prepare and compile methods"""
    def __init__(self, success: bool, message: str, verdict: RunVerdict = RunVerdict.CE):
        self.success = success
        self.message = message
        self.verdict = verdict

    @staticmethod
    def ok():
        """Return OK"""
        return UtilityRunResult(True, "OK", RunVerdict.OK)

    @staticmethod
    def err(verdict: RunVerdict, message: str):
        """Return error with verdict"""
        return UtilityRunResult(False, message, verdict)

    def to_run_result(self) -> "RunResult":
        """Convert to usual run result"""
        if self.success:
            return RunResult(0, "OK", "", RunVerdict.OK, {})
        return RunResult(1, "ERR", self.message, self.verdict, {})


class RunResult:
    """Returned by test method which runs the code"""

    return_code: int
    stdout: str
    stderr: str
    verdict: RunVerdict
    files: dict[str, str]

    def __init__(self, return_code: int, stdout: str, stderr: str,
                 verdict: RunVerdict, files: dict[str, str]):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.verdict = verdict
        self.files = files

    def to_dict(self):
        """Serialize"""
        return {"return_code": self.return_code,
                "stdout": self.stdout,
                "stderr": self.stderr,
                "verdict": self.verdict.to_string(),
                "files": self.files}


class Compiler(ABC):
    """ABC for any compiler"""

    COMPILERS: dict = {}

    file_ext: str = ""

    def __init__(self):
        pass

    def save_files(self, files_config: dict[str, str]) -> None:
        """Save solution filese"""
        for path, content in files_config.items():
            with open(f"solution/{path}", "w") as file:
                file.write(content)

    def load_files(self, files: set[str]) -> dict[str, str] | None:
        """
        Load file contents for given set of files.
        :return: dict where key - filename and value - file contents
        """
        file_dict = {}
        for file in files:
            if not os.path.exists(f"solution/{file}"):
                return None
            with open(file, "r") as handle:
                file_dict[file] = handle.read()
        return file_dict

    async def launch_and_get_output(self, file_path: str, proc_input: str,
                                    file_input: dict[str, str],
                                    required_back_files: set[str],
                                    timeout: int, mem_limit_mb: int,
                                    solution_dir: str) -> RunResult:
        """Compile and run code"""
        result = await self.prepare(file_path, file_input, required_back_files, solution_dir)
        if not result.success:
            return result.to_run_result()

        result = await self.compile(file_path, file_input, required_back_files, solution_dir)
        if not result.success:
            return result.to_run_result()

        return await self.test(file_path, proc_input, file_input,
                               required_back_files, timeout, mem_limit_mb, solution_dir)

    @abstractmethod
    async def prepare(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str], solution_dir) -> UtilityRunResult:
        """Prepare solution for compilation"""

    @abstractmethod
    async def compile(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str], solution_dir) -> UtilityRunResult:
        """Compile solution"""

    @abstractmethod
    async def test(self, file_path: str, proc_input: str,
                   file_input: dict[str, str],
                   required_back_files: set[str],
                   timeout: int, mem_limit_mb: int,
                   solution_dir) -> RunResult:
        """Run solution"""


def register_default_compilers():
    """Dependency injection mechanism"""
    for compiler_name, compiler_module in settings.COMPILERS.items():
        Compiler.COMPILERS[compiler_name] = load_class(compiler_module, Compiler)
