"""
Configuration classes
"""

import yaml
from pydantic import BaseModel

from judgeservice import judgelet, settings
from judgeservice.exceptions import ImproperlyConfiguredException, BadBalancingStrategy
from judgeservice.judgelet import JudgeletGroup, Selector, Judgelet, SingleBalancedStrategy


class JudgeletGroupModel(BaseModel):
    """Model for one variant of config"""
    name: str
    selector: str
    nodes: list[str]
    load_balancing: str


class JudgeletGroupSingleNodeModel(BaseModel):
    """Model for other variant of config"""
    name: str
    selector: str
    node: str


class Configuration:
    """Configuration file class"""
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> list[JudgeletGroup]:
        """Load and validate config"""
        with open(self.config_path, "r", encoding=settings.FILE_ENCODING) as file:
            obj = yaml.safe_load(file.read())
            if "judgelet_groups" not in obj:
                raise ImproperlyConfiguredException("No judgelet_groups key present")
            configs = [JudgeletGroupModel(**group) if "nodes" in group
                       else JudgeletGroupSingleNodeModel(**group)
                       for group in obj["judgelet_groups"]]
            groups = [
                JudgeletGroup(
                    cfg.name,
                    Selector(cfg.selector),
                    (
                        [Judgelet(addr) for addr in cfg.nodes]
                        if isinstance(cfg, JudgeletGroupModel)
                        else [Judgelet(cfg.node)]
                    ),
                    self._get_load_balancer(cfg.load_balancing
                                            if isinstance(cfg, JudgeletGroupModel)
                                            else None)
                )
                for cfg in configs
            ]
            return groups

    def _get_load_balancer(self, name: str | None):
        """Get load balancer by name"""
        if name is None:
            return SingleBalancedStrategy()
        if name not in judgelet.STRATEGIES:
            raise BadBalancingStrategy(f"No strategy with name {name}")
        return judgelet.STRATEGIES[name]()
