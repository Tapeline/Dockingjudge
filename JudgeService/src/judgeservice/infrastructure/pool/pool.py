import re
from dataclasses import dataclass
from typing import override

import structlog

from judgeservice.application.interfaces import JudgeletPool
from judgeservice.domain.entities import (
    Judgelet,
)
from judgeservice.domain.exceptions import (
    NoSuitableJudgeletFoundException,
)
from judgeservice.infrastructure.pool.strategies import (
    AbstractBalancingStrategy,
)

logger = structlog.get_logger(__name__)


class Selector:
    """Determines to which group request should be forwarded."""

    def __init__(self, selector_str: str) -> None:
        self.selector_str = selector_str

    def is_applicable(self, target: str) -> bool:
        """Check if selector is applicable to given target."""
        if self.selector_str == "*":
            return True
        match = re.fullmatch(self.selector_str, target)
        return match is not None


@dataclass
class JudgeletGroup:
    """Represents a group of judgelets."""

    selector: Selector
    nodes: list[Judgelet]


class JudgeletPoolImpl(JudgeletPool):
    """HTTP judgelet pool."""

    def __init__(
        self,
        balancing_strategy: AbstractBalancingStrategy,
        groups: list[JudgeletGroup],
    ) -> None:
        self.balance = balancing_strategy
        self.groups = groups

    @override
    async def get_for_compiler(self, compiler_name: str) -> Judgelet:
        group = self._get_group_for_compiler(compiler_name)
        node = await self.balance.get_preferred_node(group.nodes)
        if node is None:
            logger.error(
                "No judgelet found for compiler",
                compiler_name=compiler_name,
            )
            raise NoSuitableJudgeletFoundException
        return node

    def _get_group_for_compiler(self, compiler_name: str) -> JudgeletGroup:
        for group in self.groups:
            if group.selector.is_applicable(compiler_name):
                return group
        logger.error(
            "No judgelet group found for compiler",
            compiler_name=compiler_name,
        )
        raise NoSuitableJudgeletFoundException
