from typing import Any, override

from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from account_service import settings
from api import serializers
from api.exceptions import (
    PasswordTooCommonException,
    PasswordTooShortException,
    RegistrationDisabledException,
    UserAlreadyExistsException,
)
from api.models import IssuedToken, User


class RegisterView(CreateAPIView[User]):
    """Register a user."""

    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    @override
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Register a user."""
        if not settings.ALLOW_REGISTRATION:
            raise RegistrationDisabledException
        if User.objects.filter(username=request.data.get("username")).exists():
            raise UserAlreadyExistsException
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        _validate_password(password)
        return super().create(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    """Log in a user."""

    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)  # type: ignore[assignment]

    @override
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Perform log in."""
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0]) from exc

        access_token = serializer.validated_data["access"]
        user = serializer.validated_data["user"]

        IssuedToken.objects.create(user=user, token=access_token)

        return Response(
            {
                "token": access_token,
                "user_data": serializers.MyProfileSerializer(
                    user, context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )


def _validate_password(password: str) -> None:
    try:
        CommonPasswordValidator().validate(password)
    except DjangoValidationError as exc:
        raise PasswordTooCommonException from exc
    if len(password) < 8:
        raise PasswordTooShortException
