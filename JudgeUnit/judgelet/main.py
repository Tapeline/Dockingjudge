import asyncio
import sys

import structlog

if sys.platform == "win32":
    from asyncio import WindowsSelectorEventLoopPolicy

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.logging import LoggingConfig, StructLoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin

from judgelet.config import Config
from judgelet.controllers import http
from judgelet.di import AppProvider

config = Config()
container = make_async_container(
    AppProvider(),
    context={
        Config: config,
    }
)

shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.add_log_level,
    structlog.dev.set_exc_info,
]
if sys.stderr.isatty() and False:
    processors = shared_processors + [
        structlog.processors.TimeStamper(
            fmt="%Y-%m-%d %H:%M:%S", utc=False
        ),
        structlog.dev.ConsoleRenderer(),
    ]
else:
    processors = shared_processors + [
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]


def get_litestar_app() -> Litestar:
    logging_config = LoggingConfig(
        root={"level": "INFO", "handlers": ["queue_listener"]},
        formatters={
            "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        log_exceptions="always",
    )
    litestar_app = Litestar(
        debug=config.mode.debug_mode,
        route_handlers=[
            http.SolutionsController,
        ],
        openapi_config=OpenAPIConfig(
            title="Judgelet",
            description="Judgelet docs",
            version="1.0.0",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
        plugins=[
            StructlogPlugin(
                StructlogConfig(
                    StructLoggingConfig(
                        #standard_lib_logging_config=logging_config,
                        processors=processors,
                        #logger_factory=structlog.get_logger,
                        logger_factory=structlog.WriteLoggerFactory(
                            file=open("log.log", "w")
                        )
                    )
                )
            )
        ]
    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    litestar_app = get_litestar_app()
    return litestar_app


app = get_app()
