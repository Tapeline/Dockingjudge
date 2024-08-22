import requests

from solution_service import settings


class TaskMock:
    def __init__(self, task_type, task_id, data):
        self.type = task_type
        self.id = task_id
        self.data = data


def get_task(task_type, task_id) -> TaskMock | None:
    response = requests.get(
        f"{settings.CONTEST_SERVICE}"
        f"/internal/contests/tasks/{task_type}/{task_id}"
    )
    if response.status_code != 200:
        return None
    return TaskMock(
        task_type,
        task_id,
        response.json()
    )


def can_sumbit(task_type, task_id, user_id) -> dict:
    response = requests.get(
        f"{settings.CONTEST_SERVICE}"
        f"/contests/tasks/{task_type}/{task_id}/can-submit/{user_id}/"
    )
    return response.json()