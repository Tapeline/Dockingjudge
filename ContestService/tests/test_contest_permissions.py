import pytest

from api.models import Contest
from contest_service import settings
from tests.common import (
    api,
    create_client,
    create_contest,
)


@pytest.mark.django_db
def test_user_can_create_contest(author):
    client = create_client(author.token)
    settings.ALLOW_CONTEST_CREATION_TO = ["*"]
    response = client.post(
        api("/"),
        {
            "name": "New Contest",
            "description": "A new contest for testing.",
        },
        format="json",
    )
    assert response.status_code == 201
    assert Contest.objects.filter(name="New Contest").exists()


@pytest.mark.django_db
def test_user_cannot_create_contest_if_disallowed(participant):
    settings.ALLOW_CONTEST_CREATION_TO = ["admin"]
    client = create_client(participant.token)
    response = client.post(
        api("/"),
        {
            "name": "Disallowed Contest",
            "description": "This should not be created.",
        },
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_author_can_manage_contest(author):
    contest = create_contest(author.data["id"])
    client = create_client(author.token)
    response = client.get(api(f"/{contest.id}/can-manage/"))
    assert response.status_code == 200
    assert response.json() == {"can_manage": True}


@pytest.mark.django_db
def test_non_author_cannot_manage_contest(author, participant):
    contest = create_contest(author.data["id"])
    client = create_client(participant.token)
    response = client.get(api(f"/{contest.id}/can-manage/"))
    assert response.status_code == 200
    assert response.json() == {"can_manage": False}
