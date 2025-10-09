import pytest
from tests.common import api, create_client, create_contest, author


@pytest.mark.django_db
def test_create_text_page_adds_to_contest_pages(client, contest):
    response = client.post(
        api(f"/{contest.id}/tasks/text/"),
        {"name": "Introduction", "text": "Welcome to the contest."},
        format="json",
    )
    page_id = response.data["id"]
    contest.refresh_from_db()
    assert contest.pages == [{"type": "text", "id": page_id}]


@pytest.mark.django_db
def test_delete_text_page_removes_from_contest_pages(client, contest):
    response = client.post(
        api(f"{contest.id}/tasks/text/"),
        {"name": "Introduction", "text": "Welcome to the contest."},
        format="json",
    )
    page_id = response.data["id"]
    client.delete(api(f"/{contest.id}/tasks/text/{page_id}/"))
    contest.refresh_from_db()
    assert contest.pages == []


@pytest.mark.django_db
def test_create_quiz_task_adds_to_contest_pages(client, contest):
    response = client.post(
        api(f"{contest.id}/tasks/quiz/"),
        {
            "title": "Simple Math",
            "description": "What is 1 + 1?",
            "validator": {"type": "text", "args": {"pattern": "2"}},
            "points": 5,
        },
        format="json",
    )
    task_id = response.data["id"]
    contest.refresh_from_db()
    assert contest.pages == [{"type": "quiz", "id": task_id}]


@pytest.mark.django_db
def test_delete_quiz_task_removes_from_contest_pages(client, contest):
    response = client.post(
        api(f"{contest.id}/tasks/quiz/"),
        {
            "title": "Simple Math",
            "description": "What is 1 + 1?",
            "validator": {"type": "text", "args": {"pattern": "2"}},
            "points": 5,
        },
        format="json",
    )
    task_id = response.data["id"]
    client.delete(api(f"/{contest.id}/tasks/quiz/{task_id}/"))
    contest.refresh_from_db()
    assert contest.pages == []


@pytest.mark.django_db
def test_create_code_task_adds_to_contest_pages(
    client, contest, dummy_test_suite
):
    response = client.post(
        api(f"{contest.id}/tasks/code/"),
        {
            "title": "Hello, World!",
            "description": "Write a program that prints 'Hello, World!'",
            "test_suite": dummy_test_suite,
        },
        format="json",
    )
    task_id = response.data["id"]
    contest.refresh_from_db()
    assert contest.pages == [{"type": "code", "id": task_id}]


@pytest.mark.django_db
def test_delete_code_task_removes_from_contest_pages(
    client, contest, dummy_test_suite
):
    response = client.post(
        api(f"{contest.id}/tasks/code/"),
        {
            "title": "Hello, World!",
            "description": "Write a program that prints 'Hello, World!'",
            "test_suite": dummy_test_suite,
        },
        format="json",
    )
    task_id = response.data["id"]
    client.delete(api(f"/{contest.id}/tasks/code/{task_id}/"))
    contest.refresh_from_db()
    assert contest.pages == []


@pytest.mark.django_db
def test_creating_multiple_pages_updates_contest_pages(populated_contest):
    contest = populated_contest["contest"]
    contest.refresh_from_db()
    assert contest.pages == [
        {"type": "text", "id": populated_contest["text_id"]},
        {"type": "quiz", "id": populated_contest["quiz_id"]},
        {"type": "code", "id": populated_contest["code_id"]},
    ]


@pytest.mark.django_db
def test_deleting_one_of_multiple_pages_updates_contest_pages(
    client, populated_contest
):
    contest = populated_contest["contest"]
    quiz_id = populated_contest["quiz_id"]
    client.delete(api(f"/{contest.id}/tasks/quiz/{quiz_id}/"))
    contest.refresh_from_db()
    assert contest.pages == [
        {"type": "text", "id": populated_contest["text_id"]},
        {"type": "code", "id": populated_contest["code_id"]},
    ]


@pytest.mark.django_db
def test_deleting_all_pages_empties_contest_pages(client, populated_contest):
    contest = populated_contest["contest"]
    client.delete(api(f"/{contest.id}/tasks/text/{populated_contest['text_id']}/"))
    client.delete(api(f"/{contest.id}/tasks/quiz/{populated_contest['quiz_id']}/"))
    client.delete(api(f"/{contest.id}/tasks/code/{populated_contest['code_id']}/"))
    contest.refresh_from_db()
    assert contest.pages == []
