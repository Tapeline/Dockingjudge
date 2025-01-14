from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar import Litestar
from litestar.datastructures import State
from litestar.exceptions import InternalServerException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from solution_service.config import PostgresConfig


class Base(DeclarativeBase):
    pass


def create_session_maker(postgres_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}".format(
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
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
