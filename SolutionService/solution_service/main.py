import asyncio
from typing import Awaitable, Any

import uvicorn
from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations import litestar as litestar_integration
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from litestar import Litestar
from litestar.logging import LoggingConfig
from litestar.middleware.base import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi.spec import Components

from solution_service.config import Config
from solution_service.controllers import http
from solution_service.controllers.mq import mq_controller
from solution_service.di import AppProvider
from solution_service.infrastructure import account_service
from solution_service.infrastructure.account_service import ServiceAuthenticationMiddleware
from solution_service.infrastructure.rmq import create_broker

config = Config()
broker = create_broker(config.rabbitmq)
container = make_async_container(
    AppProvider(),
    context={
        Config: config,
        RabbitBroker: broker
    }
)


def get_faststream_app() -> FastStream:
    faststream_app = FastStream(broker)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(mq_controller)
    return faststream_app


def get_litestar_app() -> Litestar:
    logging_config = LoggingConfig(
        root={"level": "INFO", "handlers": ["queue_listener"]},
        formatters={
            "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        log_exceptions="always",
    )
    auth_mw = DefineMiddleware(
        ServiceAuthenticationMiddleware,
        other_services=config.services,
        exclude=["/api/v1/solutions/docs"]
    )
    litestar_app = Litestar(
        debug=config.mode.debug_mode,
        route_handlers=[
            http.SolutionsController,
            http.ping,
        ],
        openapi_config=OpenAPIConfig(
            title="Litestar Example",
            description="Example of Litestar with Scalar OpenAPI docs",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin()],
            path="/api/v1/solutions/docs",
            components=Components(
                security_schemes={**account_service.provided_security_definitions}
            )
        ),
        logging_config=logging_config,
        middleware=[auth_mw],

    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app():
    faststream_app = get_faststream_app()
    litestar_app = get_litestar_app()
    litestar_app.on_startup.append(faststream_app.broker.start)
    litestar_app.on_shutdown.append(faststream_app.broker.close)
    return litestar_app
