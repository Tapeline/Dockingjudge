from typing import AsyncIterable

from dishka import Provider, Scope, provide, AnyOf
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from solution_service.application import interfaces
from solution_service.application.interfaces.storage import Storage
from solution_service.config import Config
from solution_service.infrastructure import persistence
from solution_service.infrastructure.persistence import s3_service


class PersistenceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(
        self, config: Config
    ) -> async_sessionmaker[AsyncSession]:
        return persistence.database.create_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[
        AsyncSession,
        interfaces.storage.DBSession,
    ]]:
        async with session_maker() as session:
            yield session

    solution_repo = provide(
        persistence.repo_impl.SolutionRepoImpl,
        scope=Scope.REQUEST,
        provides=interfaces.solutions.SolutionRepository
    )

    storage_impl = provide(
        s3_service.S3Storage,
        provides=Storage,
        scope=Scope.APP
    )
