"""
API endpoints
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, get_object_or_404,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView,
                                     ListAPIView)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from account_service import settings
from api import serializers, rmq
from api import models
from api.exceptions import RegistrationDisabledException, UserAlreadyExistsException
from api.models import User


class PingView(APIView):
    def get(self, request):
        # pylint: disable=unused-argument
        return HttpResponse("ok", content_type="text/plain")


class RegisterView(CreateAPIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if not settings.ALLOW_REGISTRATION:
            raise RegistrationDisabledException
        if User.objects.filter(username=request.data.get("username")).exists():
            raise UserAlreadyExistsException
        return super().create(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        access_token = serializer.validated_data['access']
        user = serializer.validated_data['user']

        # pylint: disable=no-member
        models.IssuedToken.objects.create(user=user, token=access_token)

        return Response(
            {
                'token': access_token,
                "user_data": serializers.MyProfileSerializer(
                    user, context={'request': request}
                ).data
            },
            status=status.HTTP_200_OK
        )


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.MyProfileSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user_data = serializers.UserSerializer(self.request.user).data
        response = super().delete(request, *args, **kwargs)
        rmq.notify_user_deleted(user_data)
        return response


class GetUserByNameView(APIView):
    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        return Response(
            serializers.UserSerializer(
                get_object_or_404(models.User, username=kwargs["username"])
            ).data,
            status=200
        )


class SetProfilePictureView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfilePicSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user


class GetAllUsersView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if "id" in self.request.query_params:
            ids = [int(i) for i in self.request.query_params.getlist("id")]
            qs = qs.filter(id__in=ids)
        return qs
