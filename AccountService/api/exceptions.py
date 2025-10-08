from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
    PermissionDenied,
)


class RegistrationDisabledException(PermissionDenied):
    """Raised when user tries to register when registration is disallowed."""

    detail = ErrorDetail(
        "Registration temporarily disabled",
        code="REGISTRATION_DISABLED",
    )


class UserAlreadyExistsException(APIException):
    """Raised when user tries to register when this username already taken."""

    detail = ErrorDetail(
        "User with such name is already registered",
        code="ALREADY_REGISTERED",
    )
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordTooShortException(APIException):
    """Raised when password is too short."""

    detail = ErrorDetail(
        "Password too short",
        code="PASSWORD_TOO_SHORT",
    )
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordTooCommonException(APIException):
    """Raised when password is too common."""

    detail = ErrorDetail(
        "Password too common",
        code="PASSWORD_TOO_COMMON",
    )
    status_code = status.HTTP_400_BAD_REQUEST
