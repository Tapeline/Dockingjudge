from behave import given, when, then

from features.environment import get_client


def _get_task_data(task_type: str, name: str, **kwargs):
    if task_type == "text":
        return {
            "name": name,
            "text": "Default text",
            **kwargs
        }
    if task_type == "quiz":
        return {
            "title": name,
            "description": "Default quiz description",
            "points": 10,
            "validator": {
                "type": "text",
                "args": {
                    "pattern": ""
                }
            },
            **kwargs
        }
    if task_type == "code":
        return {
            "title": name,
            "description": "Default code description",
            "test_suite": {
                "groups": [],
                "precompile": [],
                "time_limit": 1,
                "mem_limit_mb": 256,
                "public_cases": [],
                "compile_timeout": 5
            }
        }


def _create_task(context, task_type, name, extra_data):
    payload = _get_task_data(task_type, name, **extra_data)
    response = get_client(context).post(
        f"v1/contests/{context.contest_id}/tasks/{task_type}/",
        json=payload
    ).raise_for_status()
    context.response = response
    context.page_id = response.json()["id"]
    context.page_type = task_type


@when('creates {page_type} page "{page_name}"')
def impl(context, page_type, page_name):
    _create_task(context, page_type, page_name, {})


@given('created {page_type} page "{page_name}"')
def impl(context, page_type, page_name):
    _create_task(context, page_type, page_name, {})


@then('contest pages contain "{page_name}"')
def impl(context, page_name):
    client = get_client(context)
    response = client.get(
        f"v1/contests/{context.contest_id}/"
    ).raise_for_status()
    page_names = [
        page["content"].get("name") or page["content"].get("title")
        for page in response.json()["pages"]
    ]
    assert page_name in page_names


@then('contest pages do not contain "{page_name}"')
def impl(context, page_name):
    client = get_client(context)
    response = client.get(
        f"v1/contests/{context.contest_id}/"
    ).raise_for_status()
    page_names = [
        page.get("name") or page.get("title")
        for page in response.json()["pages"]
    ]
    assert page_name not in page_names


@when("sets the page's {field} to {value}")
def impl(context, field, value):
    context.response = get_client(context).patch(
        f"v1/contests/{context.contest_id}"
        f"/tasks/{context.page_type}/{context.page_id}/",
        json={field: eval(value)}
    )


@then("the page's {field} is now {value}")
def impl(context, field, value):
    page = get_client(context).get(
        f"v1/contests/{context.contest_id}"
        f"/tasks/{context.page_type}/{context.page_id}/"
    ).raise_for_status().json()
    assert page.get(field, None) == eval(value), page


@when("deletes the page")
def impl(context):
    context.response = get_client(context).delete(
        f"v1/contests/{context.contest_id}"
        f"/tasks/{context.page_type}/{context.page_id}/"
    )
