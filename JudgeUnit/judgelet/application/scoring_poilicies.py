"""Impl of scoring policies."""

from operator import attrgetter
from types import MappingProxyType
from typing import Final, Sequence

from judgelet.domain.results import Verdict
from judgelet.domain.test_group import ScoringPolicy


class GradualScoringPolicy(ScoringPolicy):
    def get_score(self, full_score: int, verdicts: Sequence[Verdict]) -> int:
        tests_total = len(verdicts)
        tests_passed = len(list(filter(
            attrgetter("is_successful"), verdicts
        )))
        return int(full_score * (tests_passed / tests_total))


class PolarScoringPolicy(ScoringPolicy):
    def get_score(self, full_score: int, verdicts: Sequence[Verdict]) -> int:
        if all(map(attrgetter("is_successful"), verdicts)):
            return full_score
        return 0


POLICIES: Final = MappingProxyType({
    "graded": GradualScoringPolicy,
    "polar": PolarScoringPolicy
})
