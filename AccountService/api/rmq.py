"""
Module for working with rabbitmq
"""

import json

import pika

from account_service import settings


USER_OBJECT_EXCHANGE = "user_object_events"


def init():
    """Initialize rabbitmq"""
    connection = _connect()
    channel = connection.channel()
    _init_exchange(channel)
    connection.close()


def _init_exchange(channel):
    """Initialize exchange we're responsible for"""
    channel.exchange_declare(exchange=USER_OBJECT_EXCHANGE, durable=True)


def _connect():
    """Connect to configured rabbitmq"""
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RMQ_ADDRESS,
        port=5672,
        credentials=pika.PlainCredentials(
            username=settings.RMQ_USER,
            password=settings.RMQ_PASS
        )
    ))


def publish_message(exchange: str, routing_key: str, data: dict) -> None:
    """Connect and publish a rabbitmq message. A blocking call"""
    connection = _connect()
    channel = connection.channel()
    _init_exchange(channel)
    json_str = json.dumps(data)
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=json_str.encode(settings.ENCODING))
    connection.close()


def notify_user_deleted(user_data: dict) -> None:
    """Publish notification about deleted user"""
    publish_message(USER_OBJECT_EXCHANGE, "user_event", {
        "event": "DELETED",
        "object": user_data
    })
