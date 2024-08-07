import json

import pika

from contest_service import settings


CONTEST_OBJECT_EXCHANGE = "contest_object_events"


def _init_exchange(channel):
    channel.exchange_declare(exchange=CONTEST_OBJECT_EXCHANGE, durable=True)


def connect():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RMQ_ADDRESS,
        port=5672,
        credentials=pika.PlainCredentials(
            username=settings.RMQ_USER,
            password=settings.RMQ_PASS
        )
    ))


def publish_message(exchange: str, routing_key: str, data: dict) -> None:
    connection = connect()
    channel = connection.channel()
    _init_exchange(channel)
    json_str = json.dumps(data)
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=json_str.encode(settings.ENCODING))
    connection.close()

