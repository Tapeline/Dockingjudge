"""
DRF serializers
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "profile_pic"]


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "settings", "profile_pic"]


class UserProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "profile_pic"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # pylint: disable=abstract-method
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["user"] = self.user
        return data
