from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class SubmissionType(Enum):
    STR = "str"
    ZIP = "zip"


class VerdictSchema(BaseModel):
    codename: str
    is_successful: bool
    details: str


class GroupProtocolSchema(BaseModel):
    score: int
    verdicts: list[VerdictSchema]
    is_successful: bool
    verdict: VerdictSchema


@dataclass
class Solution:
    type GroupName = str

    id: str
    solution_data: bytes | None
    solution_url: str
    main_file: str | None
    submission_type: SubmissionType
    compiler: str
    suite: dict

    short_verdict: str
    group_scores: dict[GroupName, int]
    detailed_verdict: str
    protocol: dict[str, GroupProtocolSchema]
    score: int


class JudgeletAnswer(BaseModel):
    """Response model."""

    score: int
    verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, GroupProtocolSchema]
    compilation_error: str | None = None



class Judgelet(ABC):
    def __init__(self, address: str):
        self.address = address
        self._opened_connections = 0

    @abstractmethod
    async def is_alive(self) -> bool:
        """Check if judgelet is reachable and responding."""
        raise NotImplementedError

    @abstractmethod
    async def check_solution(self, solution: Solution) -> JudgeletAnswer:
        """Perform solution checking."""
        raise NotImplementedError

    def notify_opened_connection(self) -> None:
        """Count connections for load balancing."""
        self._opened_connections += 1

    def notify_closed_connection(self) -> None:
        """Count connections for load balancing."""
        self._opened_connections = max(self._opened_connections - 1, 0)

    @property
    def opened_connections(self) -> int:
        """Count connections for load balancing."""
        return self._opened_connections
