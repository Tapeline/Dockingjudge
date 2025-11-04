from datetime import datetime, timedelta, timezone

from behave import given, when, then

from features.environment import get_client
from features.steps.login_register import get_user_id


@given('created contest "{contest_name}" that starts in future')
def step_impl(context, contest_name):
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(days=1)
    context.contest_id = get_client(context).post(
        "v1/contests/",
        json={
            "name": contest_name,
            "description": "Test contest",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }
    ).raise_for_status().json()["id"]


@given('created contest "{contest_name}" that has ended')
def step_impl(context, contest_name):
    end_time = datetime.now(timezone.utc) - timedelta(days=1)
    start_time = end_time - timedelta(days=1)
    context.contest_id = get_client(context).post(
        "v1/contests/",
        json={
            "name": contest_name,
            "description": "Test contest",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }
    ).raise_for_status().json()["id"]


@when('participates in contest')
def step_impl(context):
    client = get_client(context)
    context.response = client.post(f"v1/contests/{context.contest_id}/apply/")


@given('participates in contest')
def step_impl(context):
    client = get_client(context)
    client.post(f"v1/contests/{context.contest_id}/apply/").raise_for_status()


@then('user "{username}" is a participant of the contest')
def step_impl(context, username):
    client = get_client(context)
    user_id = get_user_id(context, username)
    participants_response = client.get(f"v1/contests/{context.contest_id}/participants/")
    participants_response.raise_for_status()
    participant_ids = participants_response.json()
    assert user_id in participant_ids
