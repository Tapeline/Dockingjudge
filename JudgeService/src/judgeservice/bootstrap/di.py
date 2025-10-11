from dishka import Provider, Scope, from_context, provide

from judgeservice.application.interactors import ProcessSolutionInteractor
from judgeservice.application.interfaces import JudgeletPool, SolutionGateway
from judgeservice.config import Config
from judgeservice.infrastructure.solutions import SolutionGatewayImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    pool = from_context(provides=JudgeletPool, scope=Scope.APP)

    solution_gateway = provide(
        SolutionGatewayImpl,
        scope=Scope.APP,
        provides=SolutionGateway,
    )

    process_solution_interactor = provide(
        ProcessSolutionInteractor,
        scope=Scope.REQUEST,
    )
