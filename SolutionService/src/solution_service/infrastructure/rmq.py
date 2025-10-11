import structlog
from faststream.rabbit import RabbitBroker
from faststream.security import SASLPlaintext

from solution_service.config import RabbitMQConfig


def create_broker(rabbitmq_config: RabbitMQConfig) -> RabbitBroker:
    return RabbitBroker(
        host=rabbitmq_config.host,
        port=rabbitmq_config.port,
        security=SASLPlaintext(
            username=rabbitmq_config.username,
            password=rabbitmq_config.password,
        ),
        virtualhost="/",
        logger=structlog.get_logger("rabbit"),
    )
