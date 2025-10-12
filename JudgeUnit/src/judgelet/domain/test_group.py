from abc import abstractmethod
from collections.abc import Sequence
from operator import attrgetter
from typing import Protocol

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
        """
        Check if group was successful.

        A group is successful only if all tests in it are successful.

        """
        return all(map(attrgetter("is_successful"), self.verdicts))

    @property
    def verdict(self) -> Verdict:
        """
        Get group verdict.

        First unsuccessful verdict or OK if all are successful.

        """
        return next(
            filter(lambda verdict: not verdict.is_successful, self.verdicts),
            Verdict.OK(),
        )


class ScoringPolicy(Protocol):
    """Determines how many points should a solution get."""

    @abstractmethod
    def get_score(self, full_score: int, verdicts: Sequence[Verdict]) -> int:
        """Get a score based on how many tests of a group passed."""
        raise NotImplementedError


@frozen
class TestGroup:
    """Represents a test group entity."""

    name: str
    test_cases: Sequence[TestCase]
    full_score: int
    scoring_policy: ScoringPolicy

    async def run(self, runner: SolutionRunner) -> GroupProtocol:
        """Run test group."""
        verdicts: list[Verdict] = []
        passed_count = 0
        for case in self.test_cases:
            case_verdict = await case.run(runner)  # noqa: WPS476
            verdicts.append(case_verdict)
            passed_count += case_verdict.is_successful
        return GroupProtocol(
            self.scoring_policy.get_score(self.full_score, verdicts),
            verdicts,
        )
