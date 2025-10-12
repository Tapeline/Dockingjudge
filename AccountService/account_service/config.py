from dataclasses import dataclass, field

from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource


@dataclass(frozen=True)
class PostgresConfig:
    """Postgres configuration."""

    host: str = "localhost"
    port: int = 5503
    username: str = "pguser"
    password: str = "pgpass"  # noqa: S105
    database: str = "account_db"


@dataclass(frozen=True)
class RabbitMQConfig:
    """RMQ configuration."""

    host: str = "localhost"
    port: int = 5672
    username: str = "rm_user"
    password: str = "rm_password"  # noqa: S105


@dataclass(frozen=True)
class AppConfig:
    """App configuration."""

    allow_registration: bool = True


@dataclass(frozen=True)
class SecurityConfig:
    """Security configuration."""

    allowed_hosts: list[str] = field(
        default_factory=lambda: ["*"],
    )
    secret_key: str = (
        "django-insecure-e!dhn4o+qii7k+^sj&!2t(!1!su4=9ly#hh@h3$m06qhp&98$5"  # noqa: S105
    )


@dataclass(frozen=True)
class Config:
    """Main configuration."""

    postgres: PostgresConfig
    rabbit: RabbitMQConfig
    security: SecurityConfig
    app: AppConfig
    mode: str = "local"


service_config_loader = config_loader(
    YamlSource("account_service.yml"),
    EnvSource(prefix="ACCOUNT_SVC_", sep="__"),
    config=Config,
)
