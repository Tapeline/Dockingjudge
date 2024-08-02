import os
from abc import abstractmethod, ABC
from enum import Enum


class RunVerdict(Enum):
    OK = 0
    TL = 1
    REQUIRED_FILE_NOT_FOUND = 2
    ML = 3
    CE = 4  # Compilation error
    PF = 5  # Pre-check fail

    def to_string(self):
        if self == RunVerdict.OK:
            return "OK"
        elif self == RunVerdict.TL:
            return "TL"
        elif self == RunVerdict.REQUIRED_FILE_NOT_FOUND:
            return "PE"
        elif self == RunVerdict.ML:
            return "ML"
        elif self == RunVerdict.CE:
            return "CE"
        elif self == RunVerdict.PF:
            return "PF"


class UtilityRunResult:
    def __init__(self, success: bool, message: str, verdict: RunVerdict = RunVerdict.CE):
        self.success = success
        self.message = message
        self.verdict = verdict

    @staticmethod
    def ok():
        return UtilityRunResult(True, "OK", RunVerdict.OK)

    @staticmethod
    def err(verdict: RunVerdict, message: str):
        return UtilityRunResult(False, message, verdict)

    def to_run_result(self) -> "RunResult":
        if self.success:
            return RunResult(0, "OK", "", RunVerdict.OK, {})
        else:
            return RunResult(1, "ERR", self.message, self.verdict, {})


class RunResult:
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
        return {"return_code": self.return_code,
                "stdout": self.stdout,
                "stderr": self.stderr,
                "verdict": self.verdict.to_string(),
                "files": self.files}


class Compiler(ABC):
    COMPILERS: dict = {}

    file_ext: str = ""

    def __init__(self):
        pass

    def save_files(self, files_config: dict[str, str]) -> None:
        for path, content in files_config.items():
            with open(f"solution/{path}", "w") as file:
                file.write(content)

    def load_files(self, files: set[str]) -> dict[str, str] | None:
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
                                    timeout: int, mem_limit_mb: int) -> RunResult:
        result = await self.prepare(file_path, file_input, required_back_files)
        if not result.success:
            return result.to_run_result()

        result = await self.compile(file_path, file_input, required_back_files)
        if not result.success:
            return result.to_run_result()

        return await self.test(file_path, proc_input, file_input,
                               required_back_files, timeout, mem_limit_mb)

    @abstractmethod
    async def prepare(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str]) -> UtilityRunResult:
        pass

    @abstractmethod
    async def compile(self, file_path: str, file_input: dict[str, str],
                      required_back_files: set[str]) -> UtilityRunResult:
        pass

    @abstractmethod
    async def test(self, file_path: str, proc_input: str,
                   file_input: dict[str, str],
                   required_back_files: set[str],
                   timeout: int, mem_limit_mb: int) -> RunResult:
        pass


def register_default_compilers():
    from judgelet.compilers.python_compiler import PythonInterpreter
    Compiler.COMPILERS["python"] = PythonInterpreter
