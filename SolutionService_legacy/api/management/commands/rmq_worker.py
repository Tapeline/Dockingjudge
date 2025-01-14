import json
import logging

import pika
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from api import rmq, models
from solution_service import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection: pika.BlockingConnection = rmq.connect()
        self.channel = connection.channel()
        print("Waiting for RMQ messages")
        self.declare_bind_consume(
            queue="_solution_service_inbox",
            exchange=rmq.CHECKED_SOLUTIONS_EXCHANGE,
            key="solution_answer",
            callback=self.callback
        )
        self.declare_bind_consume(
            queue="_solution_service_inbox_user",
            exchange="user_object_events",
            key="user_event",
            callback=self.callback_user_event
        )
        self.declare_bind_consume(
            queue="_solution_service_inbox_contest",
            exchange="contest_object_events",
            key="contest_event",
            callback=self.callback_contest_event
        )
        self.declare_bind_consume(
            queue="_solution_service_inbox_quiz_task",
            exchange="contest_object_events",
            key="quiz_task_event",
            callback=self.callback_quiz_task_event
        )
        self.declare_bind_consume(
            queue="_solution_service_inbox_code_task",
            exchange="contest_object_events",
            key="code_task_event",
            callback=self.callback_code_task_event
        )
        self.channel.start_consuming()

    def declare_bind_consume(self, queue, exchange, key, callback, durable=True):
        self.channel.queue_declare(queue, durable=durable)
        self.channel.queue_bind(queue, exchange, key)
        self.channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=callback)

    @staticmethod
    def callback(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        try:
            task_type, task_id, solution_id = data["answer_to"].split("/")
            solution = models.CodeSolution.objects.get(id=int(solution_id))
        except ObjectDoesNotExist:
            logging.error(
                "Received solution answer for %s, but solution not found",
                data["answer_to"]
            )
            return
        if not data["is_successful"]:
            logging.error(
                "Solution %s check failed: %s, %s",
                data["answer_to"], data["code"], data["details"]
            )
            solution.status = solution.Status.INTERNAL_ERROR
            solution.save()
            return
        solution.status = solution.Status.CHECKED
        solution.verdict = data["contents"]["verdict"]
        solution.is_solved = data["contents"]["verdict"] == "OK"
        solution.protocol = data["contents"]["protocol"]
        solution.group_points = data["contents"]["group_scores"]
        solution.points = data["contents"]["score"]
        solution.save()
        logging.info("Successfully saved answer for %s", data["answer_to"])

    @staticmethod
    def callback_user_event(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            models.purge_objects_of_user(data["object"]["id"])

    @staticmethod
    def callback_contest_event(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            for page in data["object"]["pages"]:
                if page["type"] == "code":
                    models.purge_objects_of_code_task(page["id"])
                elif page["type"] == "quiz":
                    models.purge_objects_of_quiz_task(page["id"])

    @staticmethod
    def callback_quiz_task_event(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            models.purge_objects_of_quiz_task(data["object"]["id"])

    @staticmethod
    def callback_code_task_event(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            models.purge_objects_of_code_task(data["object"]["id"])
