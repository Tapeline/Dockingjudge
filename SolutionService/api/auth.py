import requests
from rest_framework import authentication

from solution_service import settings


class UserMock:
    def __init__(self, uid, username, usettings, pfp):
        self.settings: dict = usettings
        self.id: int = uid
        self.username: str = username
        self.pfp: str = pfp
        self.is_authenticated = True


class RemoteAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        bearer_string: str = request.META.get('HTTP_AUTHORIZATION')
        if bearer_string is None:
            return None
        response = requests.get(
            f"{settings.ACCOUNT_SERVICE}/authorize",
            headers={
                "Authorization": bearer_string
            }
        )
        if response.status_code == 200:
            data = response.json()
            return UserMock(
                data["id"],
                data["username"],
                data["settings"],
                data["profile_pic"]
            ), None
        return None
