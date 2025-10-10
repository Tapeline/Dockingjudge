from typing import Any, override

import requests
from rest_framework import authentication
from rest_framework.request import Request

from contest_service import settings


class User:
    """Resembles a user."""

    def __init__(
        self,
        uid: int,
        username: str,
        usettings: dict[str, Any],
        pfp: str | None = None,
    ) -> None:
        self.settings = usettings
        self.id = uid
        self.username = username
        self.pfp = pfp
        self.is_authenticated = True


class RemoteAuthentication(authentication.BaseAuthentication):
    """Authenticate user using account service."""

    @override
    def authenticate(self, request: Request) -> tuple[User, Any] | None:
        """Perform authentication and return user object."""
        bearer_string = request.META.get("HTTP_AUTHORIZATION")
        if not isinstance(bearer_string, str):
            return None
        response = requests.get(
            f"{settings.ACCOUNT_SERVICE}/authorize",
            headers={
                "Authorization": bearer_string,
            },
            timeout=5,
        )
        if response.status_code == 200:
            data = response.json()
            return User(
                data["id"],
                data["username"],
                data["settings"],
                data["profile_pic"],
            ), None
        return None
