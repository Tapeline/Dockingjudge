import random

import pytest

from tests.common import api

_DUMMY_QUIZ_TASK_FIELDS = {
    "validator": {"type": "text", "args": {"pattern": "test"}},
    "points": 100,
}


@pytest.mark.parametrize(
    "tasks",
    [
        [
            ("quiz", "A"),
            ("quiz", "B"),
            ("quiz", "C"),
        ],
        [
            ("code", "A"),
            ("code", "B"),
            ("code", "C"),
        ],
        [
            ("code", "A"),
            ("quiz", "B"),
            ("code", "C"),
            ("quiz", "D"),
        ],
        [
            ("code", "D"),
            ("quiz", "B"),
            ("code", "C"),
            ("quiz", "A"),
        ],
    ],
)
@pytest.mark.django_db
def test_get_all_tasks_preserves_ordering(
    client, contest, tasks, dummy_test_suite,
):
    random_creation_order = tasks[:]
    random.shuffle(random_creation_order)
    tasks_order = []
    expected_tasks = []
    for task_type, task_title in random_creation_order:
        json_data = {
            "title": task_title,
            "description": "Test",
        }
        if task_type == "code":
            json_data["test_suite"] = dummy_test_suite
        else:
            json_data |= _DUMMY_QUIZ_TASK_FIELDS
        response = client.post(
            api(f"{contest.id}/tasks/{task_type}/"),
            json_data,
            format="json",
        )
        expected_tasks.append(response.json() | {"type": task_type})
        tasks_order.append(
            {"type": task_type, "id": response.json().get("id")},
        )
    client.patch(api(f"/{contest.id}/"), json={"pages": tasks_order})
    response = client.get(f"/internal/contests/{contest.id}/tasks/")
    assert response.json() == expected_tasks
