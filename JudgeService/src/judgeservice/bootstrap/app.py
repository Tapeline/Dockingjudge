import logging

from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream

from judgeservice.application.interfaces import JudgeletPool
from judgeservice.bootstrap.config import load_pool_impl, service_config_loader
from judgeservice.bootstrap.di import AppProvider
from judgeservice.config import Config
from judgeservice.controllers.mq import mq_controller
from judgeservice.infrastructure.rmq import create_broker

logger = logging.getLogger(__name__)


def get_app() -> FastStream:
    """Bootstrap faststream app."""
    config = service_config_loader.load()
    broker = create_broker(config.rabbitm)
    pool = load_pool_impl(config)
    container = make_async_container(
        AppProvider(),
        context={
            Config: config,
            JudgeletPool: pool,
        },
    )
    faststream_app = FastStream(broker, logger=logger)
    broker.include_router(mq_controller)
    faststream_integration.setup_dishka(
        container, faststream_app, auto_inject=True,
    )
    return faststream_app
