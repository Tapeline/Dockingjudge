import os

from pydantic import Field, BaseModel


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RMQ_HOST", default="localhost")
    port: int = Field(alias="RMQ_PORT", default=5672)
    username: str = Field(alias="RMQ_USER", default="rm_user")
    password: str = Field(alias="RMQ_PASS", default="rm_pass")


class PostgresConfig(BaseModel):
    host: str = Field(alias="DB_HOST", default="localhost")
    port: int = Field(alias="DB_PORT", default=5503)
    username: str = Field(alias="DB_USER", default="pguser")
    password: str = Field(alias="DB_PASSWORD", default="pgpass")
    database: str = Field(alias="DB_NAME", default="solution_db")


class MinioConfig(BaseModel):
    host: str = Field(alias="S3_HOST", default="http://127.0.0.1")
    port: int = Field(alias="S3_PORT", default=9900)
    username: str = Field(alias="S3_USER", default="minio_user")
    password: str = Field(alias="S3_PASS", default="minio_pass")
    bucket_name: str = "solutions"
    outer_url: str = Field(
        alias="S3_OUTER_URL",
        default="http://localhost/files"
    )


class ModeConfig(BaseModel):
    debug_mode: bool = Field(alias="DEBUG", default=True)


class OtherServicesConfig(BaseModel):
    account_service: str = Field(
        alias="ACCOUNT_SERVICE",
        default="http://localhost:8001/api/v1/accounts"
    )
    contest_service: str = Field(
        alias="CONTEST_SERVICE",
        default="http://localhost:8002/api/v1",
    )
    contest_service_internal: str = Field(
        alias="CONTEST_SERVICE_INTERNAL",
        default="http://localhost:8002/internal",
    )


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field(
        default_factory=lambda: RabbitMQConfig(**os.environ)
    )
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ)
    )
    s3: MinioConfig = Field(
        default_factory=lambda: MinioConfig(**os.environ)
    )
    mode: ModeConfig = Field(
        default_factory=lambda: ModeConfig(**os.environ)
    )
    services: OtherServicesConfig = Field(
        default_factory=lambda: OtherServicesConfig(**os.environ)
    )
    encoding: str = "UTF-8"
