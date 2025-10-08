from collections.abc import Callable
from typing import Any, cast, override

from django.db.models.query import QuerySet
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import rmq, serializers
from api.models import User


class ProfileView(RetrieveUpdateDestroyAPIView[User]):
    """Get, update or delete my profile."""

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.MyProfileSerializer
    notification_function: Callable[[dict[str, Any]], None] = (
        rmq.notify_user_deleted
    )

    @override
    def get_object(self) -> User:
        """Link object to request user."""
        # IsAuthenticated is provided, so no AnonymousUser:
        return cast(User, self.request.user)

    @override
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete my profile."""
        user_data = serializers.UserSerializer(self.get_object()).data
        response = super().delete(request, *args, **kwargs)
        ProfileView.notification_function(user_data)
        return response


@extend_schema_view(
    get=extend_schema(
        responses={
            200: serializers.MyProfileSerializer,
            401: {},
        },
    ),
)
class AuthorizeView(RetrieveAPIView[User]):
    """Check for authorization."""

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MyProfileSerializer

    @override
    def get_object(self) -> User:
        """Link object to request user."""
        # IsAuthenticated is provided, so no AnonymousUser:
        return cast(User, self.request.user)


@extend_schema_view(
    get=extend_schema(
        responses=serializers.UserSerializer,
    ),
)
class GetUserByNameView(APIView):
    """Get user's profile."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get user's profile by its name."""
        return Response(
            serializers.UserSerializer(
                get_object_or_404(
                    User, username=kwargs["username"],
                ),
            ).data,
            status=status.HTTP_200_OK,
        )


class SetProfilePictureView(UpdateAPIView[User]):
    """Set my profile picture."""

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfilePicSerializer
    parser_classes = (MultiPartParser, FormParser)

    @override
    def get_object(self) -> User:
        """Link object to request user."""
        # IsAuthenticated is provided, so no AnonymousUser:
        return cast(User, self.request.user)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="User ID list",
                type={
                    "type": "array",
                    "items": {
                        "type": "integer",
                    },
                },
            ),
        ],
    ),
)
class GetAllUsersView(ListAPIView[User]):
    """Get all users (filtered)."""

    permission_classes = (AllowAny, )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    @override
    def get_queryset(self) -> QuerySet[User]:
        """Filter users by ids that were provided in query_params."""
        qs = super().get_queryset()
        if "id" in self.request.query_params:
            ids = [int(i) for i in self.request.query_params.getlist("id")]
            qs = qs.filter(id__in=ids)
        return qs
