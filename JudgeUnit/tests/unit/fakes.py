from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, ClassVar

from judgelet.application.interfaces import (
    LanguageBackendFactory,
    SandboxFactory,
)
from judgelet.domain.checking import NoArgs, Validator
from judgelet.domain.execution import LanguageBackend, SolutionRunner
from judgelet.domain.files import File, FileSystem, Solution
from judgelet.domain.results import ExitState, RunResult, Verdict
from judgelet.domain.sandbox import Sandbox, SandboxExitCause, SandboxResult
from judgelet.domain.test_case import TestCase


class _FakeCompilerBase(LanguageBackend):
    fake_prepare_result: ClassVar[RunResult] = RunResult.blank_ok()
    fake_compile_result: ClassVar[RunResult] = RunResult.blank_ok()
    fake_run_result: ClassVar[RunResult] = RunResult.blank_ok()

    async def prepare(
        self,
        fs: FileSystem,
        target_file: str,
        sandbox: Sandbox,
    ) -> RunResult:
        return self.fake_prepare_result

    async def compile(
        self,
        fs: FileSystem,
        target_file: str,
        compile_timeout_s: float,
        sandbox: Sandbox,
    ) -> RunResult:
        return self.fake_compile_result

    async def run(
        self,
        stdin: str,
        timeout_s: float,
        mem_limit_mb: float,
        sandbox: Sandbox,
    ) -> RunResult:
        return self.fake_run_result


class FakeOkCompiler(_FakeCompilerBase):
    ...


class FakePrepareErrorCompiler(_FakeCompilerBase):
    fake_prepare_result = RunResult(
        stdout="preparation error",
        stderr="preparation error",
        return_code=1,
        state=ExitState.ERROR,
    )


class FakeCompileErrorCompiler(_FakeCompilerBase):
    fake_compile_result = RunResult(
        stdout="compilation error",
        stderr="compilation error",
        return_code=1,
        state=ExitState.ERROR,
    )


class FakeRuntimeErrorCompiler(_FakeCompilerBase):
    fake_run_result = RunResult(
        stdout="runtime error",
        stderr="runtime error",
        return_code=1,
        state=ExitState.ERROR,
    )


class FakeCompileTimeLimitCompiler(_FakeCompilerBase):
    fake_compile_result = RunResult(
        stdout="",
        stderr="",
        return_code=1,
        state=ExitState.TIME_LIMIT,
    )


class FakeCompileMemoryLimitCompiler(_FakeCompilerBase):
    fake_compile_result = RunResult(
        stdout="",
        stderr="",
        return_code=1,
        state=ExitState.MEM_LIMIT,
    )


class FakeRunTimeLimitCompiler(_FakeCompilerBase):
    fake_run_result = RunResult(
        stdout="",
        stderr="",
        return_code=1,
        state=ExitState.TIME_LIMIT,
    )


class FakeRunMemoryLimitCompiler(_FakeCompilerBase):
    fake_run_result = RunResult(
        stdout="",
        stderr="",
        return_code=1,
        state=ExitState.MEM_LIMIT,
    )


class _FakeValidatorBase(Validator[NoArgs]):
    args_cls = NoArgs
    fake_verdict: ClassVar[Verdict]

    def __init__(self) -> None:
        super().__init__(NoArgs())

    def validate(
        self,
        result: RunResult,
        test_case: "TestCase",
        output_files: Mapping[str, str],
    ) -> Verdict:
        return self.fake_verdict


class FakeOkValidator(_FakeValidatorBase):
    fake_verdict = Verdict.OK()


class FakeWrongAnswerValidator(_FakeValidatorBase):
    fake_verdict = Verdict.WA()


class FakePresentErrorValidator(_FakeValidatorBase):
    fake_verdict = Verdict.PE()


class FakeFileSystem(FileSystem):
    def __init__(self, files: dict[str, str] | None = None):
        self.files = {}
        if files:
            self.files = {
                filename: File(filename, contents)
                for filename, contents in files.items()
            }

    def place_solution(self, solution: Solution) -> Path:
        for file in solution.files:
            self.files[file.name] = file
        return Path()

    def cleanup(self, solution: Solution) -> None:
        self.files.clear()

    def get_file(self, path: str) -> File | None:
        return self.files.get(path)

    def save_file(self, file: File) -> None:
        self.files[file.name] = file

    def delete_file(self, filename: str) -> None:
        self.files.pop(filename, None)


class FakeSandbox(Sandbox):
    def __init__(self, fs: FileSystem):
        super().__init__(fs, "")

    async def run(
        self,
        cmd: str,
        proc_input: str,
        timeout_s: float,
        memory_limit_mb: float,
    ) -> SandboxResult:
        return SandboxResult(
            return_code=0,
            cause=SandboxExitCause.PROCESS_EXITED,
            stderr="",
            stdout="",
        )

    def close(self):
        ...

    def destroy(self):
        ...


class FakeEmptySolution(Solution):
    def __init__(self):
        super().__init__("")

    @property
    def files(self) -> Sequence[File]:
        return [File("main.py", "")]

    @property
    def main_file_name(self) -> str | None:
        return None


def create_fake_empty_runner():
    fs = FakeFileSystem()
    return SolutionRunner(
        FakeOkCompiler(),
        FakeEmptySolution(),
        fs,
        FakeSandbox(fs),
    )


class FakeCompilerFactory(LanguageBackendFactory):
    def __init__(
        self,
        compiler_cls: Any,
        **compiler_args: Any,
    ) -> None:
        self.compiler_cls = compiler_cls
        self.compiler_args = compiler_args

    def create_backend(
        self,
        name: str,
        solution: Solution,
    ) -> LanguageBackend | None:
        return self.compiler_cls(**self.compiler_args)


class FakeSandboxFactory(SandboxFactory):
    def __call__(
        self,
        fs: FileSystem,
        sandbox_dir: str,
        encoding: str | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> Sandbox:
        return FakeSandbox(fs)


class FakeCompilerWorksOnlyIfFilePresent(_FakeCompilerBase):
    """Compiles successfully only if specified files are present.

    Used for file placement testing purposes.

    """

    def __init__(self, expected_files: dict[str, str]) -> None:
        self.expected_files = expected_files

    async def compile(
        self,
        fs: FileSystem,
        target_file: str,
        compile_timeout_s: float,
        sandbox: Sandbox,
    ) -> RunResult:
        return _ensure_files_placed(self.expected_files, fs)


class FakeCompilerWorksOnlyIfFilePresentInRuntime(_FakeCompilerBase):
    """Runs successfully only if specified files are present.

    Used for file placement testing purposes.

    """

    def __init__(self, expected_files: dict[str, str]) -> None:
        self.expected_files = expected_files

    async def run(
        self,
        stdin: str,
        timeout_s: float,
        mem_limit_mb: float,
        sandbox: Sandbox,
    ) -> RunResult:
        return _ensure_files_placed(self.expected_files, sandbox.fs)


def _ensure_files_placed(
    expected_files: dict[str, str],
    fs: FileSystem,
):
    for filename, contents in expected_files.items():
        fs_file = fs.get_file(filename)
        if not fs_file or fs_file.contents != contents:
            return RunResult(
                stdout=f"file {filename} assertion failed",
                stderr=f"file {filename} assertion failed",
                return_code=1,
                state=ExitState.ERROR,
            )
    return RunResult.blank_ok()
