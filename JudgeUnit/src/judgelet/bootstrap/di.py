from dishka import Provider, from_context, Scope, provide

from judgelet.application.interactors import CheckSolutionInteractor
from judgelet.application.interfaces import (
    LanguageBackendFactory,
    SandboxFactory,
)
from judgelet.config import Config
from judgelet.domain.files import FileSystem
from judgelet.infrastructure.filesystem import RealFileSystem
from judgelet.infrastructure.languages.factory import (
    DefaultLanguageBackendFactory
)
from judgelet.infrastructure.sandboxes.simple import SimpleSandboxFactory


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    lbr = provide(
        DefaultLanguageBackendFactory,
        provides=LanguageBackendFactory,
        scope=Scope.APP
    )

    sandbox_factory = provide(
        SimpleSandboxFactory,
        provides=SandboxFactory,
        scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    def provide_fs(self) -> FileSystem:
        return RealFileSystem()

    interactor = provide(
        CheckSolutionInteractor,
        scope=Scope.REQUEST
    )
