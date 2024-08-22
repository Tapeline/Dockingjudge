import json
import logging

import pika
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from api import rmq, models
from contest_service import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection: pika.BlockingConnection = rmq.connect()
        channel = connection.channel()
        print("Waiting for RMQ messages")
        channel.queue_declare("_solution_service_inbox", durable=True)
        channel.queue_bind(
            "_solution_service_inbox",
            rmq.CHECKED_SOLUTIONS_EXCHANGE,
            "solution_answer"
        )
        channel.basic_consume(
            queue='_solution_service_inbox',
            auto_ack=True,
            on_message_callback=self.callback
        )
        channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        task_type, task_id, solution_id = data["answer_to"].split("/")
        try:
            solution = models.Solution.objects.get(id=int(solution_id))
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
