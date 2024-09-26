"""
Provides tools for managing judgelets
"""

import re
from abc import abstractmethod, ABC
from typing import Union

import requests

from judgeservice.exceptions import NoJudgeletsSpecifiedException


class AbstractBalancingStrategy(ABC):
    """Strategy for load balancing"""
    @abstractmethod
    def get_preferred_node(self, nodes: list["Judgelet"]) -> "Judgelet":
        """
        Load balancing method.
        It is guaranteed that nodes list has at least 2 nodes
        """
        raise NotImplementedError


class SingleBalancedStrategy(AbstractBalancingStrategy):
    """Dummy balancing strategy"""
    def get_preferred_node(self, nodes: list["Judgelet"]) -> "Judgelet":
        return nodes[0]


class RoundRobinBalancingStrategy(AbstractBalancingStrategy):
    """Classic round-robin implementation"""
    def __init__(self):
        self._ptr = 0

    def get_preferred_node(self, nodes: list["Judgelet"]) -> Union["Judgelet", None]:
        beginning = self._ptr
        while True:
            node = nodes[self._ptr]
            self._ptr += 1
            if self._ptr >= len(nodes):
                self._ptr = 0
            if node.is_alive():
                return node
            if self._ptr == beginning:
                return None


class LeastConnectionsBalancingStrategy(AbstractBalancingStrategy):
    """Prefers node with the least number of connections opened"""
    def get_preferred_node(self, nodes: list["Judgelet"]) -> "Judgelet":
        nodes = list(filter(lambda n: n.is_alive(), nodes))
        if len(nodes) == 0:
            return None
        least_conn = nodes[0].get_opened_connections_count()
        selected_node = nodes[0]
        for node in nodes:
            if least_conn > (new_least_conn := node.get_opened_connections_count()):
                least_conn = new_least_conn
                selected_node = node
        return selected_node


STRATEGIES = {
    "round-robin": RoundRobinBalancingStrategy,
    "least-connections": LeastConnectionsBalancingStrategy
}


class Selector:
    """
    Selector class. Determines to which
    group request should be forwarded
    """
    def __init__(self, selector_str: str):
        self.selector_str = selector_str

    def is_applicable(self, target: str) -> bool:
        """Check if selector is applicable to given target"""
        if self.selector_str == "*":
            return True
        match = re.fullmatch(self.selector_str, target)
        return match is not None


class JudgeletGroup:
    """Represents a judgelet group"""
    def __init__(self, name: str, selector: Selector,
                 nodes: list["Judgelet"],
                 load_balancer: AbstractBalancingStrategy):
        self.name = name
        self.selector = selector
        self.nodes = nodes
        for node in nodes:
            node.group = self
        self.load_balancer = load_balancer
        if len(nodes) == 0:
            raise NoJudgeletsSpecifiedException

    def get_judgelet(self) -> "Judgelet":
        """
        Get preferred judgelet to direct request
        to based on load balancing strategy
        """
        if len(self.nodes) == 1:
            return self.nodes[0]
        return self.load_balancer.get_preferred_node(self.nodes)


class Judgelet:
    """Represents one judgelet"""
    def __init__(self, address: str):
        self.group = None
        self.address = address
        self._opened_connections = 0

    def is_alive(self) -> bool:
        """Check if judgelet is reachable and responding"""
        response = requests.get(self.address + "/ping", timeout=10)
        return response.text == "ok" and response.status_code == 200

    def notify_opened_connection(self) -> None:
        """Count connections for Least Connections load balancing"""
        self._opened_connections += 1

    def notify_closed_connection(self) -> None:
        """Count connections for Least Connections load balancing"""
        self._opened_connections = max(self._opened_connections - 1, 0)

    def get_opened_connections_count(self) -> int:
        """Count connections for Least Connections load balancing"""
        return self._opened_connections
