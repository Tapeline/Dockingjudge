"""
Provides API exception classes
"""
# pylint: disable=missing-class-docstring

from rest_framework import status
from rest_framework.exceptions import PermissionDenied, APIException


class RegistrationDisabledException(PermissionDenied):
    detail = "Registration temporarily disabled"
    code = "REGISTRATION_DISABLED"


class UserAlreadyExistsException(APIException):
    detail = "User with such name is already registered"
    code = "ALREADY_REGISTERED"
    status_code = status.HTTP_400_BAD_REQUEST
