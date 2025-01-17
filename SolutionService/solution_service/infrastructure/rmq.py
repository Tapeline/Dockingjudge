from faststream.rabbit import RabbitBroker
from faststream.security import SASLPlaintext

from solution_service.application.interfaces.publisher import AbstractSolutionPublisher
from solution_service.config import RabbitMQConfig
from solution_service.domain.entities.abstract import CodeSolution


def create_broker(rabbitmq_config: RabbitMQConfig) -> RabbitBroker:
    return RabbitBroker(
        host=rabbitmq_config.host,
        port=rabbitmq_config.port,
        security=SASLPlaintext(
            username=rabbitmq_config.username,
            password=rabbitmq_config.password,
        ),
        virtualhost="/",
    )
