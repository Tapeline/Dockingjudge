"""Abstractions for compilers"""

import os
from abc import ABC, abstractmethod
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
        """Create run result"""
        self.success = success
        self.message = message
        self.verdict = verdict

    @staticmethod
    def ok():
        """Return OK"""
        return UtilityRunResult(success=True, message="OK", verdict=RunVerdict.OK)

    @staticmethod
    def err(verdict: RunVerdict, message: str):
        """Return error with verdict"""
        return UtilityRunResult(success=False, message=message, verdict=verdict)

    def to_run_result(self) -> "RunResult":
        """Convert to usual run result"""
        if self.success:
            return RunResult(
                return_code=0,
                stdout="OK",
                stderr="",
                verdict=RunVerdict.OK,
                files={}
            )
        return RunResult(
            return_code=1,
            stdout="ERR",
            stderr=self.message,
            verdict=self.verdict,
            files={}
        )


class RunResult:
    """Returned by test method which runs the code"""

    return_code: int
    stdout: str
    stderr: str
    verdict: RunVerdict
    files: dict[str, str]

    def __init__(  # noqa: WPS211 (too many args)
            self,
            return_code: int,
            stdout: str,
            stderr: str,
            verdict: RunVerdict,
            files: dict[str, str]
    ):
        """Create run result"""
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.verdict = verdict
        self.files = files

    def to_dict(self):
        """Serialize"""
        return {
            "return_code": self.return_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "verdict": self.verdict.to_string(),
            "files": self.files
        }


class AbstractCompiler(ABC):
    """ABC for any compiler"""

    COMPILERS: dict = {}

    file_ext: str = ""

    def __init__(self, context: dict | None = None):
        """Create compiler and initialize context"""
        if context is None:
            context = {}
        self._context = context

    def save_files(self, files_config: dict[str, str]) -> None:
        """Save solution files"""
        for path, file_content in files_config.items():
            with open(f"solution/{path}", "w") as solution_file:
                solution_file.write(file_content)

    def load_files(self, files: set[str]) -> dict[str, str] | None:
        """
        Load file contents for given set of files.
        Args:
            files: file paths
        Returns:
            dict where key - filename and value - file contents
        """
        file_dict = {}
        for solution_file in files:
            if not os.path.exists(f"solution/{solution_file}"):
                return None
            with open(solution_file, "r") as file_handle:
                file_dict[solution_file] = file_handle.read()
        return file_dict

    async def launch_and_get_output(  # noqa: WPS211 (too many args)
            self,
            file_path: str,
            proc_input: str,
            file_input: dict[str, str],
            required_back_files: set[str],
            timeout: int,
            mem_limit_mb: int,
            solution_dir: str
    ) -> RunResult:
        """Test code"""
        return await self.run_solution(
            file_path,
            proc_input,
            file_input,
            required_back_files,
            timeout,
            mem_limit_mb,
            solution_dir
        )

    @abstractmethod
    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        """Prepare solution for compilation"""
        raise NotImplementedError

    @abstractmethod
    async def compile(
            self,
            file_path: str,
            compile_timeout: int,
            solution_dir: str
    ) -> UtilityRunResult:
        """Compile solution"""
        raise NotImplementedError

    @abstractmethod
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
        """Run solution"""
        raise NotImplementedError


def register_default_compilers():
    """Dependency injection mechanism"""
    for compiler_name, compiler_module in settings.COMPILERS.items():
        AbstractCompiler.COMPILERS[compiler_name] = load_class(compiler_module, AbstractCompiler)
