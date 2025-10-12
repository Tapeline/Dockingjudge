from dishka import Provider, Scope, from_context

from solution_service.config import Config


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
