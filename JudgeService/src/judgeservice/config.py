from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    """Configuration for RabbitMQ."""

    host: str = "localhost"
    port: int = 5672
    username: str = "rm_user"
    password: str = "rm_password"  # noqa: S105


@dataclass(frozen=True, slots=True)
class S3Config:
    """S3 connection configuration."""

    base_url: str = "http://localhost:9900"


@dataclass(frozen=True, slots=True)
class JudgeletGroupModel:
    """Group of judgelets."""

    name: str
    selector: str
    nodes: list[str] | str


@dataclass(frozen=True, slots=True)
class JudgeletPoolConfig:
    """Pool configuration."""

    groups: list[JudgeletGroupModel]
    load_balancing: str
    consider_dead_after_timeout_s: int = 5


@dataclass(frozen=True, slots=True)
class Config:
    """App configuration."""

    rabbitmq: RabbitMQConfig
    s3: S3Config
    pool: JudgeletPoolConfig
    judgelet_endpoint_format: str = "{0}/run"
