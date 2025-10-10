import json
from typing import Any, Final

import pika

from contest_service import settings

CONTEST_OBJECT_EXCHANGE: Final = "contest_object_events"


def init() -> None:
    """Initialize rabbitmq."""
    connection = connect()
    channel = connection.channel()
    _init_exchange(channel)
    connection.close()


def _init_exchange(
    channel: pika.adapters.blocking_connection.BlockingChannel,
) -> None:
    """Initialize exchange we're responsible for."""
    channel.exchange_declare(exchange=CONTEST_OBJECT_EXCHANGE, durable=True)


def connect() -> pika.BlockingConnection:
    """Connect to configured rabbitmq."""
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RMQ_ADDRESS,
            port=settings.RMQ_PORT,
            credentials=pika.PlainCredentials(
                username=settings.RMQ_USER,
                password=settings.RMQ_PASS,
            ),
        ),
    )


def publish_message(
    exchange: str, routing_key: str, data: dict[str, Any],
) -> None:
    """Connect and publish a rabbitmq message. A blocking call."""
    connection = connect()
    channel = connection.channel()
    _init_exchange(channel)
    json_str = json.dumps(data)
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=json_str.encode(settings.ENCODING),
    )
    connection.close()


def notify_contest_deleted(data: dict[str, Any]) -> None:
    """Notify a contest was deleted."""
    # TODO: maybe refactor to transactional outbox
    publish_message(
        CONTEST_OBJECT_EXCHANGE,
        "contest_event",
        _deleted_event(data),
    )


def notify_text_page_deleted(data: dict[str, Any]) -> None:
    """Notify a text page was deleted."""
    # TODO: maybe refactor to transactional outbox
    publish_message(
        CONTEST_OBJECT_EXCHANGE,
        "text_page_event",
        _deleted_event(data),
    )


def notify_quiz_task_deleted(data: dict[str, Any]) -> None:
    """Notify a quiz task was deleted."""
    # TODO: maybe refactor to transactional outbox
    publish_message(
        CONTEST_OBJECT_EXCHANGE,
        "quiz_task_event",
        _deleted_event(data),
    )


def notify_code_task_deleted(data: dict[str, Any]) -> None:
    """Notify a code task was deleted."""
    # TODO: maybe refactor to transactional outbox
    publish_message(
        CONTEST_OBJECT_EXCHANGE,
        "code_task_event",
        _deleted_event(data),
    )


def _deleted_event(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "event": "DELETED",
        "object": data,
    }
