import json

import pika

from account_service import settings


USER_OBJECT_EXCHANGE = "user_object_events"


def _init_exchange(channel):
    channel.exchange_declare(exchange=USER_OBJECT_EXCHANGE, durable=True)


def _connect():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RMQ_ADDRESS,
        port=5672,
        credentials=pika.PlainCredentials(
            username=settings.RMQ_USER,
            password=settings.RMQ_PASS
        )
    ))


def publish_message(exchange: str, routing_key: str, data: dict) -> None:
    connection = _connect()
    channel = connection.channel()
    _init_exchange(channel)
    json_str = json.dumps(data)
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=json_str.encode(settings.ENCODING))
    connection.close()


def notify_user_deleted(user_data: dict) -> None:
    publish_message(USER_OBJECT_EXCHANGE, "user_event", {
        "event": "DELETED",
        "object": user_data
    })
