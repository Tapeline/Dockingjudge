"""Contains classes related to code execution."""

from abc import ABC, abstractmethod

from structlog import get_logger

from judgelet.domain.files import FileSystem, Solution
from judgelet.domain.results import RunResult
from judgelet.domain.sandbox import Sandbox


class LanguageBackend(ABC):
    """ABC for a language implementation."""

    @property
    @abstractmethod
    def file_ext(self) -> str:
        """Get language file extension."""
        raise NotImplementedError

    @abstractmethod
    async def prepare(self, fs: FileSystem, target_file: str) -> RunResult:
        """Prepare environment."""
        raise NotImplementedError

    @abstractmethod
    async def compile(
            self, fs: FileSystem, target_file: str, compile_timeout_s: float
    ) -> RunResult:
        """Compile the solution."""
        raise NotImplementedError

    @abstractmethod
    async def run(
            self,
            stdin: str,
            timeout_s: float,
            mem_limit_mb: float,
            sandbox: Sandbox
    ) -> RunResult:
        """Run the solution."""
        raise NotImplementedError


class SolutionRunner:
    """Wrapper for LanguageBackend"""

    def __init__(
            self,
            backend: LanguageBackend,
            solution: Solution,
            fs: FileSystem,
            sandbox: Sandbox
    ) -> None:
        """Create wrapper."""
        self.backend = backend
        self.solution = solution
        self.fs = fs
        self.sandbox = sandbox
        self.log = get_logger().bind(solution_id=solution.uid)

    async def compile(self, compilation_timeout_s: float) -> RunResult:
        """Prepare and compile the solution."""
        self.log.info("Preparing")
        main_file_name = self.solution.main_file.name
        result = await self.backend.prepare(self.fs, main_file_name)
        if not result.is_successful:
            self.log.info("Preparing failed")
            return result
        compile_result = await self.backend.compile(
            self.fs, main_file_name, compilation_timeout_s
        )
        if not compile_result.is_successful:
            self.log.info("Compilation failed")
        return compile_result

    async def run(
            self,
            stdin: str,
            timeout_s: float,
            mem_limit_mb: float
    ) -> RunResult:
        """Run the solution."""
        self.log.info("Running for %s", stdin[:min(len(stdin), 32)])
        return await self.backend.run(
            stdin, timeout_s, mem_limit_mb, self.sandbox
        )
