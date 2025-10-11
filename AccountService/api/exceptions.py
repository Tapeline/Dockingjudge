from typing import Any

from django.http.response import Http404

from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
    PermissionDenied, NotFound,
)
from rest_framework.views import set_rollback
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied


class RegistrationDisabledException(PermissionDenied):
    """Raised when user tries to register when registration is disallowed."""

    default_detail = {
        "detail": "Registration temporarily disabled",
        "code": "REGISTRATION_DISABLED",
    }
    status_code = status.HTTP_403_FORBIDDEN


class UserAlreadyExistsException(APIException):
    """Raised when user tries to register when this username already taken."""

    default_detail = {
        "detail": "User with such name is already registered",
        "code": "ALREADY_REGISTERED",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordTooShortException(APIException):
    """Raised when password is too short."""

    default_detail = {
        "detail": "Password too short",
        "code": "PASSWORD_TOO_SHORT"
    }
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordTooCommonException(APIException):
    """Raised when password is too common."""

    default_detail = {
        "detail": "Password too common",
        "code": "PASSWORD_TOO_COMMON"
    }
    status_code = status.HTTP_400_BAD_REQUEST
