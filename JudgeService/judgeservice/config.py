import os

import yaml
from dishka import FromDishka
from pydantic import BaseModel, Field

from judgeservice.exceptions import BadBalancingStrategy
from judgeservice.infrastructure.pool import (
    JudgeletGroup,
    Selector,
    JudgeletImpl,
    SingleBalancedStrategy,
    STRATEGIES,
    JudgeletPoolImpl
)


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RMQ_HOST", default="localhost")
    port: int = Field(alias="RMQ_PORT", default=5672)
    username: str = Field(alias="RMQ_USER", default="rm_user")
    password: str = Field(alias="RMQ_PASS", default="rm_password")


class S3Config(BaseModel):
    base_url: str = Field(alias="S3_BASE_URL", default="http://localhost:9900")


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field(
        default_factory=lambda: RabbitMQConfig(**os.environ)
    )
    s3: S3Config = Field(
        default_factory=lambda: S3Config(**os.environ)
    )
    judgelet_endpoint_format: str = Field(default="{0}/run-suite")
    config_path: str = Field(default="config.yml")


class JudgeletGroupModel(BaseModel):
    """Model for one variant of config"""
    name: str
    selector: str
    nodes: list[str] | str


class JudgeletConfigFile(BaseModel):
    groups: list[JudgeletGroupModel]
    load_balancing: str


class FileConfiguration:
    """Configuration file class"""
    def __init__(self, config: FromDishka[Config]):
        self.config = config

    def load_config(self) -> JudgeletPoolImpl:
        """Load pool from file config"""
        with open(self.config.config_path, "r", encoding="UTF-8") as file:
            file_cfg = JudgeletConfigFile(**yaml.safe_load(file.read()))
            groups = [
                JudgeletGroup(
                    Selector(group.selector),
                    (
                        [
                            JudgeletImpl(addr, self.config.judgelet_endpoint_format)
                            for addr in group.nodes
                        ]
                        if isinstance(group.nodes, list)
                        else [JudgeletImpl(group.nodes, self.config.judgelet_endpoint_format)]
                    )
                )
                for group in file_cfg.groups
            ]
            lb = self._get_load_balancer(file_cfg.load_balancing)
            return JudgeletPoolImpl(lb, groups)

    def _get_load_balancer(self, name: str | None):
        """Get load balancer by name"""
        if name is None:
            return SingleBalancedStrategy()
        if name not in STRATEGIES:
            raise BadBalancingStrategy(f"No strategy with name {name}")
        return STRATEGIES[name]()
