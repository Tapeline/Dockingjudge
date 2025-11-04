import time
from behave import given, when, then

from features.environment import get_client
from features.steps.login_register import (
    create_user_if_not_exists,
    login_using_stored_password,
)


def _as_manager(context):
    context.execute_steps('Given registered user "Manager"')
    context.execute_steps('Given as user "Manager"')
    #create_user_if_not_exists(context, "Manager")
    #login_using_stored_password(context, "Manager")


@given('a contest with quiz task with right answer "{answer}"')
def step_impl(context, answer):
    _as_manager(context)
    context.contest_id = get_client(context).post(
        "v1/contests/",
        json={
            "name": "Submission contest",
            "description": "...",
            "is_started": True
        }
    ).raise_for_status().json()["id"]
    response = get_client(context).post(
        f"v1/contests/{context.contest_id}/tasks/quiz/",
        json={
            "title": "Test Quiz",
            "description": "What is the answer?",
            "points": 10,
            "validator": {"type": "text", "args": {"pattern": answer}}
        }
    ).raise_for_status().json()
    context.page_id = response["id"]
    context.page_type = "quiz"


@when('submits "{solution}" as solution to the quiz task')
def step_impl(context, solution):
    context.response = get_client(context).post(
        f"v1/solutions/post/quiz/{context.page_id}/",
        json={"text": solution}
    ).raise_for_status()
    context.solution_id = context.response.json()["id"]


def _get_solution(context):
    client = get_client(context)
    for _ in range(10):
        response = client.get(f"v1/solutions/{context.solution_id}/")
        response.raise_for_status()
        solution = response.json()
        if solution["short_verdict"] != "NC":
            return solution
        time.sleep(0.5)
    raise TimeoutError("Solution did not get judged in time")


@then("solution's verdict is {verdict}")
def step_impl(context, verdict):
    solution = _get_solution(context)
    assert solution["short_verdict"] == verdict


@given('a contest with code task with test case (input "{inp}" output "{outp}")')
def step_impl(context, inp, outp):
    _as_manager(context)
    client = get_client(context)
    context.contest_id = client.post(
        "v1/contests/",
        json={
            "name": "Submission contest",
            "description": "...",
            "is_started": True
        }
    ).raise_for_status().json()["id"]
    test_suite = {
        "groups": [
            {
                "name": "group1",
                "points": 100,
                "scoring_rule": "polar",
                "depends_on": [],
                "cases": [
                    {
                        "stdin": inp,
                        "validators": [
                            {"type": "stdout", "args": {"expected": outp}}
                        ]
                    }
                ]
            }
        ],
        "precompile": [],
        "time_limit": 1.0,
        "mem_limit_mb": 256,
        "public_cases": [],
        "compile_timeout": 5
    }
    client.patch(
        f"v1/contests/{context.contest_id}/",
        json={"is_started": True}
    )
    response = client.post(
        f"v1/contests/{context.contest_id}/tasks/code/",
        json={
            "title": "Test Code",
            "description": "Solve this.",
            "test_suite": test_suite
        }
    ).raise_for_status().json()
    context.page_id = response["id"]
    context.page_type = "code"


@when('submits python "{code}" as solution to the code task')
def step_impl(context, code):
    client = get_client(context)
    context.response = client.post(
        f"v1/solutions/post/code/{context.page_id}/",
        json={
            "compiler": "python",
            "submission_type": "str",
            "text": code,
        }
    )
    context.response.raise_for_status()
    context.solution_id = context.response.json()["id"]
