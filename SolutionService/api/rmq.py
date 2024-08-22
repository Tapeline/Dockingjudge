import json

import pika

from .tasks import TaskMock
from contest_service import settings


UNCHECKED_SOLUTIONS_EXCHANGE = "solutions_exchange"
CHECKED_SOLUTIONS_EXCHANGE = "judge_answers_exchange"


def _init_exchange(channel):
    channel.exchange_declare(exchange=UNCHECKED_SOLUTIONS_EXCHANGE, durable=True)
    channel.exchange_declare(exchange=CHECKED_SOLUTIONS_EXCHANGE, durable=True)


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


def queue_code_solution(task: TaskMock, solution) -> None:
    publish_message(UNCHECKED_SOLUTIONS_EXCHANGE, "solution_to_check", {
        "id": f"{solution.task_type}/{solution.task_id}/{solution.id}",
        "code": solution.text,
        "compiler": solution.compiler,
        "suite": task.data["test_suite"]
    })