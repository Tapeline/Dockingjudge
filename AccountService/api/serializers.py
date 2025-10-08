from collections.abc import Mapping
from typing import Any, override

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models


class RegistrationSerializer(serializers.ModelSerializer[models.User]):
    """Used for incoming registration requests."""

    class Meta:
        model = models.User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}  # noqa: RUF012

    @override
    def create(self, validated_data: Mapping[str, Any]) -> models.User:
        """Create user and properly hash the password."""
        return models.User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer[models.User]):
    """Used for untrusted user responses."""

    class Meta:
        model = models.User
        fields = ("id", "username", "profile_pic")


class MyProfileSerializer(serializers.ModelSerializer[models.User]):
    """Used for trusted user responses."""

    class Meta:
        model = models.User
        fields = ("id", "username", "settings", "profile_pic")


class UserProfilePicSerializer(serializers.ModelSerializer[models.User]):
    """Used for incoming user profile picture change requests."""

    class Meta:
        model = models.User
        fields = ("id", "profile_pic")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Used for incoming login requests."""

    @override
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Inject user."""
        data = super().validate(attrs)
        data["user"] = self.user  # type: ignore[assignment]
        # TODO: figure out whether we need this line ^^^
        return data
