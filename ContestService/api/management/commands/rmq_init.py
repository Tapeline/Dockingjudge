import logging
from typing import Any

from django.core.management import BaseCommand

from api import rmq

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Initialize rmq."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Command impl."""
        rmq.init()
        logger.info("RMQ init.")
