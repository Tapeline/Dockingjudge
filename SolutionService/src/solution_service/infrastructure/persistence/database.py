from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from solution_service.config import PostgresConfig

_DATABASE_URI_TEMPLATE: Final = (
    "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}"
)
_POOL_SIZE: Final = 15
_MAX_OVERFLOW: Final = 15
_CONNECT_TIMEOUT_S: Final = 5


class Base(DeclarativeBase):
    """Base for sqlalchemy models."""


def create_session_maker(
    postgres_config: PostgresConfig,
) -> async_sessionmaker[AsyncSession]:
    database_uri = _DATABASE_URI_TEMPLATE.format(
        login=postgres_config.username,
        password=postgres_config.password,
        host=postgres_config.host,
        port=postgres_config.port,
        database=postgres_config.database,
    )

    engine = create_async_engine(
        database_uri,
        pool_size=_POOL_SIZE,
        max_overflow=_MAX_OVERFLOW,
        connect_args={
            "connect_timeout": _CONNECT_TIMEOUT_S,
        },
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False,
    )
