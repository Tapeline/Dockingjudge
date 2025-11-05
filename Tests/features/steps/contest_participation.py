from datetime import datetime, timedelta, timezone

from behave import given, when, then

from features.environment import get_client


@when('participates in contest')
def step_impl(context):
    client = get_client(context)
    context.response = client.post(f"v1/contests/{context.contest_id}/apply/")


@given('participates in contest')
def step_impl(context):
    client = get_client(context)
    client.post(f"v1/contests/{context.contest_id}/apply/").raise_for_status()
