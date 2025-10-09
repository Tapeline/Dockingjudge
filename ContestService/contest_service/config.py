from dataclasses import dataclass, field

from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource


@dataclass(frozen=True)
class PostgresConfig:
    """Postgres configuration."""

    host: str = "localhost"
    port: int = 5501
    username: str = "pguser"
    password: str = "pgpass"  # noqa: S105
    database: str = "contest_db"


@dataclass(frozen=True)
class RabbitMQConfig:
    """RMQ configuration."""

    host: str = "localhost"
    port: int = 5672
    username: str = "rm_user"
    password: str = "rm_password"  # noqa: S105


@dataclass(frozen=True)
class AvailableCompiler:
    id: str
    syntax_highlighting: str


@dataclass(frozen=True)
class AppConfig:
    """App configuration."""

    available_compilers: list[AvailableCompiler]
    allow_contest_creation_to: list[str]


@dataclass(frozen=True)
class SecurityConfig:
    """Security configuration."""

    allowed_hosts: list[str] = field(
        default_factory=lambda: ["*"],
    )
    secret_key: str = (
        'django-insecure-3&uwud=s#&0(uz**lf5$fi+m#)gf40l+s!v84l&afvi5bxqjr!'  # noqa: S105
    )


@dataclass(frozen=True)
class OtherServicesConfig:
    """Other services connections config."""

    account_service: str = "http://localhost:8001/api/v1/accounts"


@dataclass(frozen=True)
class Config:
    """Main configuration."""

    postgres: PostgresConfig
    rabbit: RabbitMQConfig
    security: SecurityConfig
    app: AppConfig
    services: OtherServicesConfig
    mode: str = "local"


service_config_loader = config_loader(
    YamlSource("contest_service.yml"),
    EnvSource(prefix="CONTEST_SVC_", sep="__"),
    config=Config,
)
