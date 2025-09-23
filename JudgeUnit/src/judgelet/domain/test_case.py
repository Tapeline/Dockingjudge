"""Contains classes related to test case."""

from collections.abc import Mapping, Collection, Sequence
from typing import TYPE_CHECKING

from judgelet.domain.execution import SolutionRunner
from judgelet.domain.files import FileIO
from judgelet.domain.results import Verdict, RunResult, ExitState

if TYPE_CHECKING:
    from judgelet.domain.checking import Validator


class TestCase:
    """Represents a single test case."""

    def __init__(
            self,
            stdin: str,
            time_limit_s: float,
            memory_limit_mb: float,
            input_files: Mapping[str, str],
            output_files: Collection[str],
            validators: Sequence["Validator"]
    ) -> None:
        """Create test case."""
        self.stdin = stdin
        self.time_limit_s = time_limit_s
        self.memory_limit_mb = memory_limit_mb
        self.input_files = input_files
        self.output_files = output_files
        self.validators = validators

    async def run(self, runner: SolutionRunner) -> Verdict:
        """Run the solution and check the answer."""
        file_io = FileIO(runner.fs, self.input_files, self.output_files)
        with file_io:
            result = await runner.run(
                self.stdin,
                self.time_limit_s,
                self.memory_limit_mb,
            )
        if result.state == ExitState.MEM_LIMIT:
            return Verdict.ML()
        if result.state == ExitState.TIME_LIMIT:
            return Verdict.TL()
        if not result.is_successful:
            return Verdict.RE(_get_error_message(result))
        return self._perform_validation(result, file_io.output_files_data)

    def _perform_validation(
            self,
            result: RunResult,
            output_files: Mapping[str, str]
    ) -> Verdict:
        """Get first validator error or OK."""
        verdicts = (
            validator.validate(result, self, output_files)
            for validator in self.validators
        )
        return next(
            (
                verdict for verdict in verdicts
                if not verdict.is_successful
            ),
            Verdict.OK()
        )


def _get_error_message(result: RunResult) -> str:
    return (
        f"-- code {result.return_code} --\n"
        f"-- stdout --\n"
        f"{result.stdout}\n\n"
        f"-- stderr --\n"
        f"{result.stderr}\n\n"
    )
