import asyncio
from abc import abstractmethod
from operator import attrgetter
from types import MappingProxyType
from typing import Final, Protocol, override

import structlog

from judgeservice.domain.entities import Judgelet

logger = structlog.get_logger(__name__)


class AbstractBalancingStrategy(Protocol):
    """Strategy for load balancing."""

    @abstractmethod
    async def get_preferred_node(
        self, nodes: list[Judgelet],
    ) -> Judgelet | None:
        """Load balancing method."""
        raise NotImplementedError


class SingleBalancedStrategy(AbstractBalancingStrategy):
    """Dummy balancing strategy."""

    @override
    async def get_preferred_node(self, nodes: list[Judgelet]) -> Judgelet:
        logger.info("Using single-node mode")
        return nodes[0]


class RoundRobinBalancingStrategy(AbstractBalancingStrategy):
    """Classic round-robin implementation."""

    def __init__(self) -> None:
        self._ptr = 0

    @override
    async def get_preferred_node(
        self, nodes: list[Judgelet],
    ) -> Judgelet | None:
        logger.info("Using round-robin strategy")
        beginning = self._ptr
        while True:
            node = nodes[self._ptr]
            self._ptr += 1
            if self._ptr >= len(nodes):
                self._ptr = 0
            if await node.is_alive():
                return node
            if self._ptr == beginning:
                return None


class LeastConnectionsBalancingStrategy(AbstractBalancingStrategy):
    """Prefers node with the least number of connections opened."""

    @override
    async def get_preferred_node(
        self, nodes: list[Judgelet],
    ) -> Judgelet | None:
        logger.info("Using least connections strategy")
        nodes_statuses = await asyncio.gather(*(
            node.is_alive() for node in nodes
        ))
        nodes_and_statuses = zip(nodes, nodes_statuses, strict=False)
        nodes = [
            node for node, is_alive in nodes_and_statuses if is_alive
        ]
        if len(nodes) == 0:
            return None
        return min(nodes, key=attrgetter("opened_connections"))


STRATEGIES: Final = MappingProxyType({
    "round-robin": RoundRobinBalancingStrategy,
    "least-connections": LeastConnectionsBalancingStrategy,
})
