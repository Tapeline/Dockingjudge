from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient

from api.models import User
from api.views.profiles import ProfileView
from tests.common import api

_COMMON_USERNAME = "dummy"
_COMMON_PASSWORD = "1234abc_!"


@pytest.fixture
def mock_profile_notificator():
    mock = Mock()
    original = ProfileView.notification_function
    ProfileView.notification_function = mock
    yield mock
    ProfileView.notification_function = original


@pytest.mark.django_db
def test_get_profile_ok():
    client = APIClient()
    user = User.objects.create_user(
        _COMMON_USERNAME,
        password=_COMMON_PASSWORD,
        settings={"some_setting": "some_value"},
    )
    client.force_authenticate(user=user)
    response = client.get(api("/profile"))
    assert response.status_code == 200
    assert response.data["username"] == _COMMON_USERNAME
    assert response.data["settings"] == {"some_setting": "some_value"}


@pytest.mark.django_db
def test_cannot_access_if_not_logged_in():
    client = APIClient()
    # do not log in
    response = client.get(api("/profile"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_modify_profile():
    client = APIClient()
    user = User.objects.create_user(
        _COMMON_USERNAME,
        password=_COMMON_PASSWORD,
        settings={"some_setting": "some_value"},
    )
    client.force_authenticate(user=user)
    client.patch(
        api("/profile"),
        data={"settings": {"some_setting": "some_other_value"}},
        format="json",
    )
    user = User.objects.get(username=_COMMON_USERNAME)
    assert user.settings == {"some_setting": "some_other_value"}


@pytest.mark.django_db
def test_delete_profile(mock_profile_notificator):
    client = APIClient()
    user = User.objects.create_user(
        _COMMON_USERNAME,
        password=_COMMON_PASSWORD,
    )
    client.force_authenticate(user=user)
    client.delete(api("/profile"))
    assert not User.objects.filter(username=_COMMON_USERNAME).exists()
    mock_profile_notificator.assert_called()
