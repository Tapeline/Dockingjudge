import sys
from typing import Any

import structlog
from faststream import context


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


shared_processors = [
    _merge_contextvars,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.add_log_level,
    structlog.dev.set_exc_info,
]


def setup_processors() -> list[Any]:
    """Setup structlog processors."""
    if sys.stderr.isatty():
        return [
            *shared_processors,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False,
            ),
            structlog.dev.ConsoleRenderer(),
        ]
    return [
        *shared_processors,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]
