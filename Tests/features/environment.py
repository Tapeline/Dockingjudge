from typing import Any, Protocol

from tests.db import purge_everything
from tests.request import DockingjudgeClient, new_client


def before_scenario(context, scenario):
    context.client = new_client()


def after_scenario(context, scenario):
    purge_everything()


def after_all(context):
    purge_everything()


def get_client(context) -> DockingjudgeClient:
    return context.client
