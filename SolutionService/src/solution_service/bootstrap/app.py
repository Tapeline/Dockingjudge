import asyncio
import pprint
import sys

import structlog
from dishka import AsyncContainer, make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations import litestar as litestar_integration
from dishka.integrations.litestar import LitestarProvider
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from litestar import Litestar
from litestar.middleware.base import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi.spec import Components
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from solution_service.bootstrap.config import service_config_loader
from solution_service.bootstrap.di.auth import AuthProvider
from solution_service.bootstrap.di.config import ConfigProvider
from solution_service.bootstrap.di.interactors import InteractorProvider
from solution_service.bootstrap.di.mq import MessageQueueProvider
from solution_service.bootstrap.di.persistence import PersistenceProvider
from solution_service.bootstrap.di.services import OuterServicesProvider
from solution_service.bootstrap.logging import configure_app_logging
from solution_service.config import Config
from solution_service.controllers import http
from solution_service.controllers.mq import mq_controller
from solution_service.infrastructure.rmq import create_broker
from solution_service.infrastructure.security import (
    ServiceAuthenticationMiddleware,
    provided_security_definitions,
)


def _create_broker(config: Config) -> RabbitBroker:
    return create_broker(config.rabbitmq)


def _create_container(config: Config, broker: RabbitBroker) -> AsyncContainer:
    return make_async_container(
        LitestarProvider(),
        ConfigProvider(),
        InteractorProvider(),
        MessageQueueProvider(),
        PersistenceProvider(),
        OuterServicesProvider(),
        AuthProvider(),
        context={
            Config: config,
            RabbitBroker: broker,
        },
    )


def _get_faststream_app(
    broker: RabbitBroker, container: AsyncContainer,
) -> FastStream:
    faststream_app = FastStream(
        broker, logger=structlog.get_logger("faststream"),
    )
    faststream_integration.setup_dishka(
        container, faststream_app, auto_inject=True,
    )
    broker.include_router(mq_controller)
    return faststream_app


def _get_litestar_app(
    config: Config,
    container: AsyncContainer,
) -> Litestar:
    prometheus_config = PrometheusConfig(
        app_name="solution_service",
        group_path=True,
        exclude=["/metrics"],
    )
    auth_mw = DefineMiddleware(
        ServiceAuthenticationMiddleware,
        other_services=config.services,
        exclude=[
            "/api/v1/solutions/docs",
            "/metrics",
        ],
    )
    litestar_app = Litestar(
        debug=config.debug_mode,
        route_handlers=[
            http.SolutionsController,
            http.ping,
            PrometheusController,
        ],
        openapi_config=OpenAPIConfig(
            title="Solution service",
            description="Solution service docs",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin()],
            path="/api/v1/solutions/docs",
            components=Components(
                security_schemes={
                    **provided_security_definitions,
                },
            ),
        ),
        logging_config=None,
        middleware=[
            prometheus_config.middleware,
            auth_mw,
        ],
    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def _print_config(config: Config) -> None:
    logger = structlog.get_logger("config loader")
    if config.logging.json:
        logger.info("Config loaded", config=config)
    else:
        logger.info("Config loaded %s", pprint.pformat(config, indent=2))


def get_app() -> Litestar:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy(),
        )
    config = service_config_loader.load()
    configure_app_logging(config)
    broker = _create_broker(config)
    container = _create_container(config, broker)
    faststream_app = _get_faststream_app(broker, container)
    litestar_app = _get_litestar_app(config, container)
    litestar_app.on_startup.append(
        faststream_app.broker.start,  # type: ignore[union-attr]
    )
    litestar_app.on_shutdown.append(
        faststream_app.broker.stop,  # type: ignore[union-attr]
    )
    litestar_app.on_startup.append(
        lambda: _print_config(config),
    )
    return litestar_app
