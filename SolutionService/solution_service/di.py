from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide, AnyOf
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from solution_service.application import interfaces, interactors
from solution_service.application.interfaces.account import AbstractAccountService
from solution_service.application.interfaces.contest import AbstractContestService
from solution_service.application.interfaces.publisher import AbstractSolutionPublisher
from solution_service.application.interfaces.storage import AbstractStorage
from solution_service.config import Config
from solution_service.controllers.mq import RMQSolutionPublisher
from solution_service.infrastructure import persistence, contest_service, account_service
from solution_service.infrastructure.persistence import s3_service


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
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
        provides=interfaces.solutions.AbstractSolutionRepository
    )

    get_best_solution_for_user_on_task_interactor = provide(
        interactors.GetBestSolutionForUserOnTask,
        scope=Scope.REQUEST
    )

    get_solution_interactor = provide(
        interactors.GetSolution,
        scope=Scope.REQUEST
    )

    get_standings_interactor = provide(
        interactors.GetStandings,
        scope=Scope.REQUEST
    )

    list_solution_for_user_interactor = provide(
        interactors.ListSolutionForUser,
        scope=Scope.REQUEST
    )

    list_solution_for_user_on_contest_interactor = provide(
        interactors.ListSolutionForUserOnContest,
        scope=Scope.REQUEST
    )

    list_solution_for_user_on_task_interactor = provide(
        interactors.ListSolutionForUserOnTask,
        scope=Scope.REQUEST
    )

    post_code_solution_interactor = provide(
        interactors.PostCodeSolution,
        scope=Scope.REQUEST
    )

    post_quiz_solution_interactor = provide(
        interactors.PostQuizSolution,
        scope=Scope.REQUEST
    )

    account_service_impl = provide(
        account_service.AccountServiceImpl,
        provides=AbstractAccountService,
        scope=Scope.APP
    )

    contest_service_impl = provide(
        contest_service.ContestServiceImpl,
        provides=AbstractContestService,
        scope=Scope.APP
    )

    storage_impl = provide(
        s3_service.S3Storage,
        provides=AbstractStorage,
        scope=Scope.APP
    )

    publisher_impl = provide(
        RMQSolutionPublisher,
        provides=AbstractSolutionPublisher,
        scope=Scope.APP
    )
