from django.core.management import BaseCommand

from api import rmq


class Command(BaseCommand):
    def handle(self, *args, **options):
        rmq.init()
        print("RMQ init.")
