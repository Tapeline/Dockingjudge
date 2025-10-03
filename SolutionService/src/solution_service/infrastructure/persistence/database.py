from typing import Final

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from solution_service.config import PostgresConfig

_DATABASE_URI_TEMPLATE: Final = (
    "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}"
)


class Base(DeclarativeBase):
    pass


def create_session_maker(
    postgres_config: PostgresConfig
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
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
