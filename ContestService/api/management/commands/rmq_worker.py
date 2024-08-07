import json

import pika
from django.core.management import BaseCommand

from api import rmq, models
from contest_service import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection: pika.BlockingConnection = rmq.connect()
        channel = connection.channel()
        print("Waiting for RMQ messages")
        channel.queue_declare("_contest_service_inbox", durable=True)
        channel.queue_bind(
            "_contest_service_inbox",
            "user_object_events",
            "user_event"
        )
        channel.basic_consume(
            queue='_contest_service_inbox',
            auto_ack=True,
            on_message_callback=self.callback
        )
        channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            models.purge_objects_of_user(data["object"]["id"])
