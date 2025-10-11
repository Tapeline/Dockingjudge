import structlog
from faststream.rabbit import RabbitBroker
from faststream.security import SASLPlaintext

from judgeservice.config import RabbitMQConfig

logger = structlog.get_logger(__name__)


def create_broker(rabbitmq_config: RabbitMQConfig) -> RabbitBroker:
    """Create a RabbitMQ broker."""
    return RabbitBroker(
        host=rabbitmq_config.host,
        port=rabbitmq_config.port,
        security=SASLPlaintext(
            username=rabbitmq_config.username,
            password=rabbitmq_config.password,
        ),
        virtualhost="/",
        logger=logger,
    )
