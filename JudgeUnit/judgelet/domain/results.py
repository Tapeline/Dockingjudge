from enum import Enum
from typing import Self

from attrs import frozen


class ExitState(Enum):
    FINISHED = 0
    ERROR = 1
    TIME_LIMIT = 2
    MEM_LIMIT = 3


@frozen
class RunResult:
    stdout: str
    stderr: str
    return_code: int
    state: ExitState

    @staticmethod
    def blank_ok() -> "RunResult":
        return RunResult("", "", 0, ExitState.FINISHED)

    @property
    def is_successful(self) -> bool:
        return self.return_code == 0 and self.state == ExitState.FINISHED


@frozen
class Verdict:
    codename: str
    is_successful: bool
    details: str

    @classmethod
    def OK(cls) -> Self:
        """Shorthand for OK verdict."""
        return Verdict("OK", is_successful=True, details="OK")

    @classmethod
    def WA(cls, detail: str | None = None) -> Self:
        """Shorthand for Wrong Answer."""
        return Verdict("WA", is_successful=False, details=detail or "WA")

    @classmethod
    def TL(cls) -> Self:
        """Shorthand for Time Limit."""
        return Verdict("TL", is_successful=False, details="TL")

    @classmethod
    def ML(cls) -> Self:
        """Shorthand for Memory Limit."""
        return Verdict("ML", is_successful=False, details="ML")

    @classmethod
    def RE(cls, detail: str | None = None) -> Self:
        """Shorthand for Runtime Error."""
        return Verdict("RE", is_successful=False, details=detail or "RE")

    @classmethod
    def PE(cls, detail: str | None = None) -> Self:
        """Shorthand for Presentation Error."""
        return Verdict("PE", is_successful=False, details=detail or "PE")

    @classmethod
    def PCF(cls, detail: str | None = None) -> Self:
        """Shorthand for Precompile Check Fail."""
        return Verdict("PCF", is_successful=False, details=detail or "PCF")

    @classmethod
    def CE(cls, detail: str | None = None) -> Self:
        """Shorthand for Compilation Error."""
        return Verdict("CE", is_successful=False, details=detail or "CE")
