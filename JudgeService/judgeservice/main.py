from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream

from judgeservice.config import Config
from judgeservice.controllers.mq import mq_controller
from judgeservice.di import AppProvider
from judgeservice.infrastructure.rmq import create_broker

config = Config()
broker = create_broker(config.rabbitmq)
container = make_async_container(
    AppProvider(),
    context={
        Config: config,
    }
)


def get_app() -> FastStream:
    faststream_app = FastStream(broker)
    broker.include_router(mq_controller)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    return faststream_app
