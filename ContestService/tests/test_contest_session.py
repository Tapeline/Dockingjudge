import pytest
from freezegun import freeze_time

from api.models import ContestSession
from tests.common import (
    api, create_client, create_contest, author,
    participant, create_quiz_task,
)


@pytest.mark.django_db
def test_apply_for_contest_successfully(author, participant):
    contest = create_contest(author.data["id"], is_started=True)
    client = create_client(participant.token)
    response = client.post(api(f"/{contest.pk}/apply/"))
    assert response.status_code == 204
    assert ContestSession.objects.filter(
        user=participant.data["id"], contest=contest
    ).exists()


@pytest.mark.parametrize(
    "params",
    [
        {"is_started": False, "is_ended": False},
        {"is_started": True, "is_ended": True},
        {"is_started": False, "is_ended": True},  # kinda impossible but nvm
    ]
)
@pytest.mark.django_db
def test_cannot_apply_non_running_contest(author, participant, params):
    contest = create_contest(author.data["id"], **params)
    client = create_client(participant.token)
    response = client.post(api(f"/{contest.pk}/apply/"))
    assert response.status_code == 403
    assert not ContestSession.objects.filter(
        user=participant.data["id"], contest=contest
    ).exists()


@pytest.mark.django_db
def test_cannot_apply_for_contest_twice(author, participant):
    contest = create_contest(author.data["id"], is_started=True)
    client = create_client(participant.token)
    client.post(api(f"/{contest.id}/apply/"))
    response = client.post(api(f"/{contest.id}/apply/"))
    assert response.status_code == 403


@pytest.mark.django_db
@freeze_time("2025-01-01 12:00:00")
def test_get_time_left(author, participant):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=3600,
        is_started=True,
    )
    client = create_client(participant.token)
    client.post(api(f"/{contest.id}/apply/"))

    with freeze_time("2025-01-01 12:30:00"):
        response = client.get(api(f"/{contest.id}/time-left/"))
        assert response.status_code == 200
        assert response.json()["time_left"] == 1800, response.json()


@pytest.mark.django_db
@freeze_time("2025-01-01 12:00:00")
def test_no_time_left(author, participant):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=3600,
        is_started=True,
    )
    client = create_client(participant.token)
    client.post(api(f"/{contest.id}/apply/"))

    with freeze_time("2025-01-01 13:00:01"):
        response = client.get(api(f"/{contest.id}/time-left/"))
        assert response.status_code == 200
        assert response.json()["time_left"] < 0
        assert not response.json()["is_unlimited"]


@pytest.mark.django_db
@freeze_time("2025-01-01 12:00:00")
def test_cannot_submit_tasks_after_time_left(author, participant):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=1,
        is_started=True,
    )
    task = create_quiz_task(contest)
    client = create_client(participant.token)
    client.post(api(f"/{contest.id}/apply/"))

    with freeze_time("2025-01-01 12:30:00"):
        response = client.get(
            api(
                f"/tasks/quiz/{task.id}/can-submit/{participant.id}/"
            )
        )
        assert response.status_code == 200
        assert response.json() == {
            "can_submit": False,
            "reason": "CONTEST_ENDED"
        }


@pytest.mark.parametrize(
    "params",
    [
        {"is_started": False, "is_ended": False},
        {"is_started": True, "is_ended": True},
        {"is_started": False, "is_ended": True},  # kinda impossible but nvm
    ]
)
@pytest.mark.django_db
def test_cannot_submit_tasks_if_contest_is_not_running(
    author, participant, params
):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=1,
        **params,
    )
    task = create_quiz_task(contest)
    ContestSession.objects.create(
        contest=contest,
        user=participant.id
    )
    client = create_client(participant.token)

    response = client.get(
        api(
            f"/tasks/quiz/{task.id}/can-submit/{participant.id}/"
        )
    )
    assert response.status_code == 200
    assert response.json() == {
        "can_submit": False,
        "reason": "CONTEST_ENDED"
    }


@pytest.mark.django_db
@freeze_time("2025-01-01 12:00:00")
def test_cannot_submit_tasks_if_not_applied_for_contest(author, participant):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=1,
        is_started=True,
    )
    task = create_quiz_task(contest)
    client = create_client(participant.token)

    response = client.get(
        api(
            f"/tasks/quiz/{task.id}/can-submit/{participant.id}/"
        )
    )
    assert response.status_code == 200
    assert response.json() == {
        "can_submit": False,
        "reason": "NOT_REGISTERED"
    }


@pytest.mark.django_db
def test_can_submit_tasks(author, participant):
    contest = create_contest(
        author.data["id"],
        time_limit_seconds=-1,
        is_started=True,
    )
    task = create_quiz_task(contest)
    client = create_client(participant.token)
    client.post(api(f"/{contest.id}/apply/"))

    response = client.get(
        api(
            f"/tasks/quiz/{task.id}/can-submit/{participant.id}/"
        )
    )
    assert response.status_code == 200
    assert response.json() == {
        "can_submit": True,
    }
