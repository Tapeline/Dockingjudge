from enum import Enum

from attrs import frozen


class ExitState(Enum):
    """Describes what caused the test to exit."""

    FINISHED = 0
    ERROR = 1
    TIME_LIMIT = 2
    MEM_LIMIT = 3


@frozen
class RunResult:
    """Report about a single run."""

    stdout: str
    stderr: str
    return_code: int
    state: ExitState

    @staticmethod
    def blank_ok() -> "RunResult":
        """Return default blank successful result."""
        return RunResult("", "", 0, ExitState.FINISHED)

    @property
    def is_successful(self) -> bool:
        """Is run successful."""
        return self.return_code == 0 and self.state == ExitState.FINISHED


@frozen
class Verdict:
    """A brief report about a single test."""

    codename: str
    is_successful: bool
    details: str

    @classmethod
    def OK(cls) -> "Verdict":
        """Shorthand for OK verdict."""
        return Verdict("OK", is_successful=True, details="OK")

    @classmethod
    def WA(cls, detail: str | None = None) -> "Verdict":
        """Shorthand for Wrong Answer."""
        return Verdict("WA", is_successful=False, details=detail or "WA")

    @classmethod
    def TL(cls) -> "Verdict":
        """Shorthand for Time Limit."""
        return Verdict("TL", is_successful=False, details="TL")

    @classmethod
    def ML(cls) -> "Verdict":
        """Shorthand for Memory Limit."""
        return Verdict("ML", is_successful=False, details="ML")

    @classmethod
    def RE(cls, detail: str | None = None) -> "Verdict":
        """Shorthand for Runtime Error."""
        return Verdict("RE", is_successful=False, details=detail or "RE")

    @classmethod
    def PE(cls, detail: str | None = None) -> "Verdict":
        """Shorthand for Presentation Error."""
        return Verdict("PE", is_successful=False, details=detail or "PE")

    @classmethod
    def PCF(cls, detail: str | None = None) -> "Verdict":
        """Shorthand for Precompile Check Fail."""
        return Verdict("PCF", is_successful=False, details=detail or "PCF")

    @classmethod
    def CE(cls, detail: str | None = None) -> "Verdict":
        """Shorthand for Compilation Error."""
        return Verdict("CE", is_successful=False, details=detail or "CE")
