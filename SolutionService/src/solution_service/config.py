from dataclasses import dataclass


@dataclass(frozen=True)
class RabbitMQConfig:
    host: str = "localhost"
    port: int = 5672
    username: str = "rm_user"
    password: str = "rm_password"  # noqa: S105


@dataclass(frozen=True)
class PostgresConfig:
    host: str = "localhost"
    port: int = 5503
    username: str = "pguser"
    password: str = "pgpass"  # noqa: S105
    database: str = "solution_db"


@dataclass(frozen=True)
class MinioConfig:
    host: str = "http://127.0.0.1"
    port: int = 9900
    username: str = "minio_user"
    password: str = "minio_pass"  # noqa: S105
    bucket_name: str = "solutions"


@dataclass(frozen=True)
class OuterServicesConfig:
    account_service: str = "http://localhost:8001/api/v1/accounts"
    contest_service: str = "http://localhost:8002/api/v1"
    contest_service_internal: str = "http://localhost:8002/internal"


@dataclass(frozen=True)
class LoggingConfig:
    level: str = "INFO"
    json: bool = True


@dataclass(frozen=True)
class Config:
    rabbitmq: RabbitMQConfig
    postgres: PostgresConfig
    s3: MinioConfig
    services: OuterServicesConfig
    logging: LoggingConfig
    debug_mode: bool = True
    encoding: str = "UTF-8"
