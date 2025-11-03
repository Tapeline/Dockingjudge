from behave import given, when, then

from features.environment import get_client


@when('creates contest "{contest_name}"')
def impl(context, contest_name):
    context.response = get_client(context).post(
        "v1/contests/",
        json={
            "name": contest_name,
            "description": "Test contest"
        }
    )


@given('created contest "{contest_name}"')
def impl(context, contest_name):
    context.contest_id = get_client(context).post(
        "v1/contests/",
        json={
            "name": contest_name,
            "description": "Test contest"
        }
    ).raise_for_status().json()["id"]


@when('sets contest {field} {value}')
def impl(context, field, value):
    context.response = get_client(context).patch(
        f"v1/contests/{context.contest_id}/",
        json={field: eval(value)}
    )


@when('deletes contest')
def impl(context):
    context.response = get_client(context).delete(
        f"v1/contests/{context.contest_id}/",
    )


@then('contest does not exist "{contest_name}"')
def impl(context, contest_name):
    assert contest_name not in {
        contest["name"]
        for contest in get_client(context)
        .get(f"v1/contests/").raise_for_status().json()
    }
