import pytest
from rest_framework.test import APIClient

from api.models import User
from tests.common import api

_COMMON_USERNAME = "dummy"
_COMMON_PASSWORD = "1234abc_!"


@pytest.mark.django_db
def test_happy_path():
    client = APIClient()
    User.objects.create_user(_COMMON_USERNAME, password=_COMMON_PASSWORD)
    response = client.post(
        api("/login"), {
            "username": _COMMON_USERNAME,
            "password": _COMMON_PASSWORD,
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_cannot_login_when_not_exists():
    client = APIClient()
    # do not create user
    response = client.post(
        api("/login"), {
            "username": _COMMON_USERNAME,
            "password": _COMMON_PASSWORD,
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_login_using_wrong_password():
    client = APIClient()
    User.objects.create_user(_COMMON_USERNAME, password=_COMMON_PASSWORD)
    response = client.post(
        api("/login"), {
            "username": _COMMON_USERNAME,
            "password": "wrong password",
        },
    )
    assert response.status_code == 401
