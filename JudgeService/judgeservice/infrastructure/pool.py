import asyncio
import base64
import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import attrgetter
from typing import Any

import aiohttp

from judgeservice.application.interfaces import JudgeletPool
from judgeservice.domain.entities import Judgelet, Solution, JudgeletAnswer, SubmissionType
from judgeservice.domain.exceptions import NoSuitableJudgeletFoundException, BadJudgeletResponseException


class AbstractBalancingStrategy(ABC):
    """Strategy for load balancing."""

    @abstractmethod
    async def get_preferred_node(self, nodes: list[Judgelet]) -> Judgelet | None:
        """Load balancing method."""
        raise NotImplementedError


class SingleBalancedStrategy(AbstractBalancingStrategy):
    """Dummy balancing strategy."""

    async def get_preferred_node(self, nodes: list[Judgelet]) -> Judgelet:
        return nodes[0]


class RoundRobinBalancingStrategy(AbstractBalancingStrategy):
    """Classic round-robin implementation."""
    def __init__(self):
        self._ptr = 0

    async def get_preferred_node(self, nodes: list[Judgelet]) -> Judgelet | None:
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
    """Prefers node with the least number of connections opened"""
    async def get_preferred_node(self, nodes: list[Judgelet]) -> Judgelet | None:
        nodes = [node for node in nodes if await node.is_alive()]
        if len(nodes) == 0:
            return None
        return min(nodes, key=attrgetter("opened_connections"))


STRATEGIES = {
    "round-robin": RoundRobinBalancingStrategy,
    "least-connections": LeastConnectionsBalancingStrategy
}


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


class JudgeletImpl(Judgelet):
    def __init__(self, address: str, endpoint_format: str) -> None:
        super().__init__(address)
        self._endpoint_format = endpoint_format
    
    async def is_alive(self) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        f"{self.address}/ping",
                        timeout=10,
                ) as response:
                    return response.status == 200
            except asyncio.TimeoutError:
                return False

    def _form_request(self, solution: Solution) -> dict:
        request: dict[str, str | dict[str, str]] = {
            "id": solution.id,
            "compiler": solution.compiler,
            "suite": solution.suite,
        }
        if solution.submission_type == SubmissionType.STR:
            request["code"] = {
                "type": "str",
                "code": solution.solution_data.decode(errors="ignore")
            }
        elif solution.submission_type == SubmissionType.ZIP:
            request["code"] = {
                "type": "zip",
                "b64": base64.b64encode(solution.solution_data).decode(),
                "main": solution.main_file
            }
        return request

    async def check_solution(self, solution: Solution) -> JudgeletAnswer:
        async with aiohttp.ClientSession() as session:
            data = self._form_request(solution)
            async with session.post(
                    self._endpoint_format.format(self.address),
                    json=data
            ) as response:
                logging.info("Got response %s", response.status)
                if response.status != 200:
                    logging.error(
                        "Judgelet %s returned %i code. Data: %s",
                        self.address,
                        response.status,
                        await response.text()
                    )
                    raise BadJudgeletResponseException
                json_response = await response.json()
                return JudgeletAnswer(**json_response)


class JudgeletPoolImpl(JudgeletPool):
    def __init__(
            self,
            balancing_strategy: AbstractBalancingStrategy,
            groups: list[JudgeletGroup],
    ) -> None:
        self.balance = balancing_strategy
        self.groups = groups

    async def get_for_compiler(self, compiler_name: str) -> Judgelet:
        group = self._get_group_for_compiler(compiler_name)
        node = await self.balance.get_preferred_node(group.nodes)
        if node is None:
            raise NoSuitableJudgeletFoundException
        return node

    def _get_group_for_compiler(self, compiler_name: str) -> JudgeletGroup:
        for group in self.groups:
            if group.selector.is_applicable(compiler_name):
                return group
        raise NoSuitableJudgeletFoundException
