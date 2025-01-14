import requests

from solution_service import settings


class TaskMock:
    def __init__(self, task_type, task_id, data):
        self.type = task_type
        self.id = task_id
        self.data = data


def get_task(task_type, task_id) -> TaskMock | None:
    response = requests.get(
        f"{settings.CONTEST_SERVICE_INTERNAL}"
        f"/contests/tasks/{task_type}/{task_id}"
    )
    if response.status_code != 200:
        return None
    return TaskMock(
        task_type,
        task_id,
        response.json()
    )


def can_submit(task_type, task_id, user_id) -> dict:
    response = requests.get(
        f"{settings.CONTEST_SERVICE}"
        f"/contests/tasks/{task_type}/{task_id}/can-submit/{user_id}/"
    )
    return response.json()


def get_contest_participants(contest_id):
    response = requests.get(
        f"{settings.CONTEST_SERVICE}"
        f"/contests/{contest_id}/participants/"
    )
    return response.json()


def get_all_tasks(contest_id):
    response = requests.get(
        f"{settings.CONTEST_SERVICE_INTERNAL}"
        f"/contests/{contest_id}/tasks/"
    )
    if response.status_code != 200:
        return []
    return response.json()
