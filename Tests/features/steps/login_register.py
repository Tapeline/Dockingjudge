from behave import given, when, then
from features.environment import get_client


_USER_PASSWORDS = {}
_DEFAULT_PASSWORD = "Passw0rd!"


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
    _USER_PASSWORDS[username] = password


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
    _USER_PASSWORDS[username] = _DEFAULT_PASSWORD


@given('as user "{username}"')
def impl(context, username):
    if username not in _USER_PASSWORDS:
        raise ValueError("User password not found")
    response = get_client(context).post(
        "v1/accounts/login/",
        json={
            "username": username,
            "password": _USER_PASSWORDS[username]
        }
    ).raise_for_status()
    get_client(context).set_token(response.json()["token"])
