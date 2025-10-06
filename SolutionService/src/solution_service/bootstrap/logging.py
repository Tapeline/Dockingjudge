import sys
from typing import Any

import structlog
from asgi_monitor.logging import configure_logging
from faststream import context

from solution_service.config import Config


def _merge_contextvars(
    logger: structlog.types.WrappedLogger,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    event_dict["extra"] = event_dict.get(
        "extra",
        context.get_local("log_context") or {},
    )
    return event_dict


def configure_app_logging(config: Config) -> Any:
    processors = [
        _merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if config.logging.json:
        processors.append(structlog.processors.dict_tracebacks)
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    configure_logging(
        level=config.logging.level,
        json_format=config.logging.json,
        include_trace=True,
    )
    return structlog.get_logger()
