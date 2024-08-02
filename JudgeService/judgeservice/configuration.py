import yaml
from pydantic import BaseModel

from judgeservice import judgelet
from judgeservice.exceptions import ImproperlyConfiguredException, BadBalancingStrategy
from judgeservice.judgelet import JudgeletGroup, Selector, Judgelet


class ConfigModel(BaseModel):
    name: str
    selector: str
    nodes: list[str]
    load_balancing: str


class Configuration:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> list[JudgeletGroup]:
        with open(self.config_path, "r") as file:
            obj = yaml.safe_load(file.read())
            if "judgelet_groups" not in obj:
                raise ImproperlyConfiguredException("No judgelet_groups key present")
            configs = [ConfigModel(**group) for group in obj["judgelet_groups"]]
            groups = [
                JudgeletGroup(
                    cfg.name,
                    Selector(cfg.selector),
                    [Judgelet(addr) for addr in cfg.nodes],
                    self._get_load_balancer(cfg.load_balancing)
                )
                for cfg in configs
            ]
            return groups

    def _get_load_balancer(self, name: str):
        if name not in judgelet.STRATEGIES:
            raise BadBalancingStrategy(f"No strategy with name {name}")
        return judgelet.STRATEGIES[name]()
