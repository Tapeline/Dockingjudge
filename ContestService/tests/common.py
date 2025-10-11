import os

import requests
from rest_framework.test import APIClient

from api.models import Contest, QuizTask

ACCOUNT_SERVICE_URL = os.environ.get(
    "ACCOUNT_SERVICE_URL", "http://localhost:8001/api/v1/accounts",
)


def api(*url: str) -> str:
    """Constructs a URL for the ContestService API."""
    assembled = "/api/v1/contests/" + "/".join(url).strip("/")
    if assembled.endswith("/"):
        return assembled
    return f"{assembled}/"


class UserHelper:
    # I hope this AI slop thing of a test works properly

    def __init__(self, username):
        self.username = username
        self.password = "1037Abcd!"
        self.token = None
        self.id = 0
        self.data = None
        self._created = False

    def create(self):
        """Creates and logs in the user via AccountService."""
        if self._created:
            return

        try:
            requests.post(
                f"{ACCOUNT_SERVICE_URL}/register/",
                json={"username": self.username, "password": self.password},
                timeout=5,
            ).raise_for_status()
        except requests.HTTPError as e:
            # Suppress 400 errors which likely mean
            # user already exists from a previous failed run
            if e.response.status_code != 400:
                raise

        login_response = requests.post(
            f"{ACCOUNT_SERVICE_URL}/login/",
            json={"username": self.username, "password": self.password},
            timeout=5,
        )
        login_response.raise_for_status()

        self.token = login_response.json()["token"]
        self.data = login_response.json()["user_data"]
        self.id = self.data["id"]
        self._created = True

    def cleanup(self):
        """Deletes the user from AccountService."""
        if not self._created or not self.token:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            requests.delete(
                f"{ACCOUNT_SERVICE_URL}/profile/", headers=headers, timeout=5,
            )
        except requests.RequestException as e:
            print(f"Warning: Failed to clean up user {self.username}: {e}")


def create_client(token=None):
    """Creates an APIClient, optionally authenticated with a token."""
    client = APIClient()
    if token:
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


def create_contest(author_id, **kwargs):
    """Creates a contest with the given author ID."""
    return Contest.objects.create(
        author=author_id,
        name="Test Contest",
        description="A test contest",
        **kwargs,
    )


def create_quiz_task(contest, **kwargs):
    return QuizTask.objects.create(
        contest=contest,
        title="Test Task",
        description="A test task",
        validator={"type": "text", "args": {"pattern": "test"}},
        points=100,
        **kwargs,
    )
