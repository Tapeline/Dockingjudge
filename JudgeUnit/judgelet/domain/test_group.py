"""Contains classes related to test group."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from operator import attrgetter

from attrs import frozen

from judgelet.domain.execution import SolutionRunner
from judgelet.domain.results import Verdict
from judgelet.domain.test_case import TestCase


@frozen
class GroupProtocol:
    """Protocol of test group."""

    score: int
    verdicts: Sequence[Verdict]

    @property
    def is_successful(self) -> bool:
        return all(map(attrgetter("is_successful"), self.verdicts))

    @property
    def verdict(self) -> Verdict:
        return next(
            filter(lambda verdict: not verdict.is_successful, self.verdicts),
            Verdict.OK()
        )


class ScoringPolicy(ABC):
    """Determines how many points should a solution get."""

    @abstractmethod
    def get_score(self, full_score: int, verdicts: Sequence[Verdict]) -> int:
        """Get a score based on how many tests of a group passed."""
        raise NotImplementedError


class TestGroup:
    """Represents a test group entity."""

    def __init__(
            self,
            name: str,
            test_cases: Sequence[TestCase],
            full_score: int,
            scoring_policy: ScoringPolicy
    ) -> None:
        """Create test group."""
        self.name = name
        self.cases = test_cases
        self.full_score = full_score
        self.scoring_policy = scoring_policy

    async def run(self, runner: SolutionRunner) -> GroupProtocol:
        """Run test group."""
        verdicts: list[Verdict] = []
        passed_count = 0
        for case in self.cases:
            case_verdict = await case.run(runner)
            verdicts.append(case_verdict)
            passed_count += case_verdict.is_successful
        return GroupProtocol(
            self.scoring_policy.get_score(self.full_score, verdicts),
            verdicts
        )
