import pytest
from rest_framework.test import APIClient

from account_service import settings
from api.models import User
from tests.common import api

_COMMON_USERNAME = "dummy"
_COMMON_PASSWORD = "1234abc_!"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("test_register_user", "v3ry_h4rd_t0_gU355!"),
        ("longenough", _COMMON_PASSWORD),
        ("CapitalLetters", _COMMON_PASSWORD),
        ("i_love_underscores", _COMMON_PASSWORD),
    ],
)
def test_happy_path(
    username: str,
    password: str,
):
    client = APIClient()
    response = client.post(api("/register"), {
        "username": username,
        "password": password,
    })
    assert response.status_code == 201
    assert response.data["username"] == username
    assert User.objects.filter(username=username).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    [
        "i hate spaces",
        "a" * 500,  # too long,
        "не латинские символы",
    ],
)
def test_bad_username(
    username: str,
):
    client = APIClient()
    response = client.post(
        api("/register"), {
            "username": username,
            "password": _COMMON_PASSWORD,
        },
    )
    assert response.status_code == 400
    assert not User.objects.filter(username=username).exists()


@pytest.mark.parametrize(
    "password",
    [
        "aiyou",  # too short
        "12345678",  # too common
    ],
)
@pytest.mark.django_db
def test_bad_password(
    password: str,
):
    client = APIClient()
    response = client.post(
        api("/register"), {
            "username": _COMMON_USERNAME,
            "password": password,
        },
    )
    assert response.status_code == 400
    assert not User.objects.filter(username=_COMMON_USERNAME).exists()


@pytest.mark.django_db
def test_cannot_register_when_registration_disallowed():
    client = APIClient()
    settings.ALLOW_REGISTRATION = False
    response = client.post(
        api("/register"), {
            "username": _COMMON_USERNAME,
            "password": _COMMON_PASSWORD,
        },
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_cannot_register_when_already_registered():
    client = APIClient()
    User.objects.create_user(_COMMON_USERNAME, password=_COMMON_PASSWORD)
    response = client.post(
        api("/register"), {
            "username": _COMMON_USERNAME,
            "password": _COMMON_PASSWORD,
        },
    )
    assert response.status_code == 403
