import logging
from typing import Any, override

from django.core.management import BaseCommand

from api import rmq

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command impl."""

    @override
    def handle(self, *args: Any, **options: Any) -> None:
        """Run rmq init."""
        rmq.init()
        logger.info("RMQ init.")
