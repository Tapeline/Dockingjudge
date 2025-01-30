from dishka import Provider, from_context, Scope, provide

from judgeservice.application.interactors import ProcessSolutionInteractor
from judgeservice.application.interfaces import JudgeletPool, SolutionGateway
from judgeservice.config import Config, FileConfiguration
from judgeservice.infrastructure.pool import JudgeletPoolImpl
from judgeservice.infrastructure.solutions import SolutionGatewayImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    file_cfg = provide(FileConfiguration, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_pool(self, file_cfg: FileConfiguration) -> JudgeletPool:
        return file_cfg.load_config()

    solution_gateway = provide(
        SolutionGatewayImpl,
        scope=Scope.APP,
        provides=SolutionGateway
    )

    process_solution_interactor = provide(
        ProcessSolutionInteractor,
        scope=Scope.REQUEST
    )
