import asyncio

from structlog import get_logger

from attrs import frozen

from judgelet.application.interfaces import (
    LanguageBackendFactory,
    SandboxFactory,
)
from judgelet.config import Config
from judgelet.domain.execution import SolutionRunner
from judgelet.domain.files import FileSystem, Solution, File
from judgelet.domain.test_suite import TestSuite, SuiteResult


lock = asyncio.Lock()


@frozen
class CheckSolutionInteractor:
    """Checks a solution."""

    backend_factory: LanguageBackendFactory
    fs: FileSystem
    sandbox_factory: SandboxFactory
    config: Config

    async def __call__(
        self,
        backend_name: str,
        solution: Solution,
        test_suite: TestSuite
    ) -> SuiteResult:
        if self.config.enable_lock:
            async with lock:
                return await self._action(backend_name, solution, test_suite)
        else:
            return await self._action(backend_name, solution, test_suite)

    async def _action(
        self,
        backend_name: str,
        solution: Solution,
        test_suite: TestSuite
    ):
        log = get_logger().bind(solution_id=solution.uid)
        solution_root = self.fs.place_solution(solution)
        log.info("Solution placed in filesystem at %s", solution_root)
        backend = self.backend_factory.create_backend(backend_name, solution)
        log.info("Instantiated language backend %s", backend)
        sandbox = self.sandbox_factory(
            self.fs,
            str(solution_root),
            environment=test_suite.envs
        )
        log.info("Created sandbox, saving additional files")
        for filename, contents in test_suite.additional_files.items():
            self.fs.save_file(File(filename, contents))
        log.info("Saved %s additionals", len(test_suite.additional_files))
        runner = SolutionRunner(backend, solution, self.fs, sandbox)
        log.info("Running solution")
        result = await test_suite.run(runner)
        self.fs.cleanup(solution)
        log.info("Cleaned up")
        return result
