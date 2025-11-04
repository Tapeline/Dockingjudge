from behave import given, when, then
from features.environment import get_client


_USERS = {}
_DEFAULT_PASSWORD = "Passw0rd!"


def create_user_if_not_exists(context, username, password=_DEFAULT_PASSWORD):
    if username in _USERS:
        return
    get_client(context).post(
        "v1/accounts/register/",
        json={
            "username": username,
            "password": password
        }
    ).raise_for_status()
    _USERS[username] = {"password": password}


def login_using_stored_password(context, username):
    if username not in _USERS:
        raise ValueError("User password not found")
    client = get_client(context)
    response = client.post(
        "v1/accounts/login/",
        json={
            "username": username,
            "password": _USERS[username]["password"]
        }
    ).raise_for_status()
    client.set_token(response.json()["token"])

    profile = client.get("v1/accounts/profile/").raise_for_status().json()
    _USERS[username]["id"] = profile["id"]
    context.user_id = profile["id"]


@given('username "{username}", password "{password}"')
def impl(context, username, password):
    context.username = username
    context.password = password


@given('registered user "{username}" "{password}"')
def impl(context, username, password):
    get_client(context).post(
        "v1/accounts/register/",
        json={
            "username": username,
            "password": password
        }
    ).raise_for_status()
    _USERS[username] = {"password": password}


@when("user signs up")
def impl(context):
    context.response = get_client(context).post(
        "v1/accounts/register/",
        json={
            "username": context.username,
            "password": context.password
        }
    )


@when('"{username}" "{password}" logs in')
def impl(context, username, password):
    context.response = get_client(context).post(
        "v1/accounts/login/",
        json={
            "username": username,
            "password": password
        }
    )


@given('registered user "{username}"')
def impl(context, username):
    get_client(context).post(
        "v1/accounts/register/",
        json={
            "username": username,
            "password": _DEFAULT_PASSWORD
        }
    ).raise_for_status()
    _USERS[username] = {"password": _DEFAULT_PASSWORD}


@given('as user "{username}"')
def impl(context, username):
    login_using_stored_password(context, username)


def get_user_id(context, username: str) -> int:
    if username in _USERS and "id" in _USERS[username]:
        return _USERS[username]["id"]

    client = get_client(context)
    user_profile = client.get(f"v1/accounts/user/{username}/").raise_for_status().json()

    if username not in _USERS:
        _USERS[username] = {}
    _USERS[username]["id"] = user_profile["id"]

    return user_profile["id"]
