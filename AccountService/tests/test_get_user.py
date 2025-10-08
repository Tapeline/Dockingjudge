
import pytest
from rest_framework.test import APIClient

from api.models import User
from tests.common import api

_COMMON_USERNAME = "dummy"
_COMMON_PASSWORD = "1234abc_!"


def _create_users():
    return [
        User.objects.create_user(f"u{i}", password=_COMMON_PASSWORD)
        for i in range(5)
    ]


@pytest.mark.django_db
def test_list_users():
    client = APIClient()
    user_list = _create_users()
    ids = [user.pk for user in user_list]
    response = client.get(
        api("/all"), data={"id": ids},
    )
    assert response.status_code == 200
    received_ids = {resp_user["id"] for resp_user in response.data}
    assert received_ids == set(ids)


@pytest.mark.django_db
def test_list_not_found():
    client = APIClient()
    response = client.get(
        api("/all"), data={"id": [1288493943]},
        # this id does not exist
    )
    assert response.data == []
