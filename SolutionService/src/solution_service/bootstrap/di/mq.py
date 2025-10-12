from dishka import Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker

from solution_service.application.interfaces.publisher import SolutionPublisher
from solution_service.controllers.mq import RMQSolutionPublisher


class MessageQueueProvider(Provider):
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)

    publisher_impl = provide(
        RMQSolutionPublisher,
        provides=SolutionPublisher,
        scope=Scope.APP,
    )
