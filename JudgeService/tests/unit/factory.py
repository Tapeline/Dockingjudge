from typing import Any

from polyfactory.factories import DataclassFactory

from judgeservice.domain.entities import Judgelet, Solution
from judgeservice.domain.pool.pool import JudgeletGroup, JudgeletPool, Selector
from judgeservice.domain.pool.strategies import (
    AbstractBalancingStrategy,
    RoundRobinBalancingStrategy,
)
from tests.unit.fakes import FakeJudgelet


def create_judgelets(params: list[dict[str, Any]]) -> list[Judgelet]:
    return [
        FakeJudgelet(**param)
        for param in params
    ]


def create_simple_pool(
    judgelets: list[Judgelet],
    strategy: AbstractBalancingStrategy | None = None,
) -> JudgeletPool:
    return JudgeletPool(
        balancing_strategy=strategy or RoundRobinBalancingStrategy(),
        groups=[JudgeletGroup(
            selector=Selector("*"),
            nodes=judgelets,
        )],
    )


def create_multigroup_pool(
    *groups: tuple[str, Judgelet, ...],
    strategy: AbstractBalancingStrategy | None = None,
) -> JudgeletPool:
    return JudgeletPool(
        balancing_strategy=strategy or RoundRobinBalancingStrategy(),
        groups=[
            JudgeletGroup(
                selector=Selector(selector),
                nodes=create_judgelets(judgelets),
            ) for selector, *judgelets in groups
        ],
    )


class SolutionFactory(DataclassFactory[Solution]):
    __model__ = Solution
