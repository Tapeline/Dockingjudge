import json
import logging
from typing import Any

import pika
from django.core.management import BaseCommand

from api import models, rmq
from contest_service import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Consume rmq messages."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Start consumer."""
        connection: pika.BlockingConnection = rmq.connect()
        channel = connection.channel()
        logger.info("Waiting for RMQ messages")
        channel.queue_declare("_contest_service_inbox", durable=True)
        channel.queue_bind(
            "_contest_service_inbox",
            "user_object_events",
            "user_event",
        )
        channel.basic_consume(
            queue="_contest_service_inbox",
            auto_ack=True,
            on_message_callback=self.callback,
        )
        channel.start_consuming()

    @staticmethod
    def callback(_: Any, __: Any, ___: Any, body: bytes) -> None:
        """Handle message."""
        data = json.loads(body.decode(settings.ENCODING))
        if data.get("event") == "DELETED":
            models.purge_objects_of_user(data["object"]["id"])
