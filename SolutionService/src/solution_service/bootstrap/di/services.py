from dishka import Provider, Scope, provide

from solution_service.application.interfaces.account import AccountService
from solution_service.application.interfaces.contest import ContestService
from solution_service.infrastructure import contest_service, account_service


class OuterServicesProvider(Provider):
    account_service_impl = provide(
        account_service.AccountServiceImpl,
        provides=AccountService,
        scope=Scope.APP
    )

    contest_service_impl = provide(
        contest_service.ContestServiceImpl,
        provides=ContestService,
        scope=Scope.APP
    )
