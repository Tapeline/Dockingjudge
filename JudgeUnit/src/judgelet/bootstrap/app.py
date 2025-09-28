import asyncio
import sys

from judgelet.bootstrap.config import judgelet_config_loader
from judgelet.bootstrap.di import AppProvider
from judgelet.bootstrap.logging import get_structlog_plugin_def
from judgelet.config import Config
from judgelet.controllers.http import SolutionsController

if sys.platform == "win32":
    from asyncio import WindowsSelectorEventLoopPolicy

from dishka import make_async_container, AsyncContainer
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin


def _create_container(config: Config):
    return make_async_container(
        AppProvider(),
        context={
            Config: config,
        }
    )


def _create_litestar(container: AsyncContainer, config: Config) -> Litestar:
    litestar_app = Litestar(
        debug=config.debug_mode,
        route_handlers=[
            SolutionsController,
        ],
        openapi_config=OpenAPIConfig(
            title="Judgelet",
            description="Judgelet docs",
            version="1.0.0",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
        plugins=[
            get_structlog_plugin_def()
        ]
    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    config = judgelet_config_loader.load()
    container = _create_container(config)
    litestar_app = _create_litestar(container, config)
    return litestar_app
