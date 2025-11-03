import http

from behave import given, when, then


@then('response contains "{something}"')
def impl(context, something):
    assert something in context.response.text


@then('response status "{status}"')
def impl(context, status):
    status = getattr(http.HTTPStatus, status.upper().replace(" ", "_"))
    assert context.response.status_code == status
