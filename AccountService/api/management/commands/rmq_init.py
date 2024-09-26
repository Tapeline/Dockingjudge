"""
Command to initialize rabbitmq exchanges
"""

from django.core.management import BaseCommand

from api import rmq


class Command(BaseCommand):
    """Command impl"""
    def handle(self, *args, **options):
        rmq.init()
        print("RMQ init.")
