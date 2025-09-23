from dishka import Provider, from_context, Scope, provide, AnyOf

from judgelet.application.interactors import CheckSolutionInteractor
from judgelet.application.interfaces import (
    LanguageBackendRepository,
    SandboxFactory,
)
from judgelet.config import Config
from judgelet.domain.files import FileSystem
from judgelet.infrastructure.filesystem import FileSystemImpl
from judgelet.infrastructure.languages.repo import (
    LanguageBackendRepositoryImpl
)
from judgelet.infrastructure.sandboxes.simple import SimpleSandboxFactoryImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    lbr = provide(
        LanguageBackendRepositoryImpl,
        provides=LanguageBackendRepository,
        scope=Scope.APP
    )

    sandbox_factory = provide(
        SimpleSandboxFactoryImpl,
        provides=SandboxFactory,
        scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    def provide_fs(self) -> FileSystem:
        return FileSystemImpl()

    interactor = provide(
        CheckSolutionInteractor,
        scope=Scope.REQUEST
    )
