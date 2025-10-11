from http import HTTPStatus
from typing import Any, Final, cast, override

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from api import accessor, models, permissions, rmq, serializers
from api.auth import User
from api.openapi import (
    COMPILER_LIST_RESPONSE,
    PARTICIPANT_LIST_RESPONSE,
    CanIManageContestSerializer,
    ContestCreationSerializer,
    ContestPatchSerializer,
    ErrorSerializer,
    GetTimeSerializer,
)
from contest_service import settings

_CONTEST_MGMT_TAGS: Final = ("Contest management",)


@extend_schema_view(
    get=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
        responses=serializers.ContestSerializer(many=True),
    ),
    post=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
        request=ContestCreationSerializer,
        responses=serializers.ContestSerializer(),
    ),
)
class ListCreateContestView(ListCreateAPIView[models.Contest]):
    """Get all contests or create new one."""

    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (IsAuthenticated, permissions.CanCreateContest)

    @override
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create contest, author field is injected automatically."""
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
        responses=serializers.ContestSerializer,
    ),
    patch=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
        request=ContestPatchSerializer,
        responses=serializers.ContestSerializer,
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
    ),
)
class RetrieveUpdateDestroyContestView(
    RetrieveUpdateDestroyAPIView[models.Contest],
):
    """Get, update or delete a contest."""

    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnly,
    )

    @override
    def get_serializer(
        self, *args: Any, **kwargs: Any,
    ) -> BaseSerializer[models.Contest]:
        """Adjust serializer settings."""
        return super().get_serializer(
            *args,
            **kwargs,
            display_only_enter_pages=not permissions.can_view_all_pages(
                self.request.user.id, self.get_object(),
            ),
            display_sensitive_info=permissions.can_manage_contest(
                self.request.user.id, self.get_object(),
            ),
        )

    @override
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete contest and notify other services."""
        contest = self.get_object()
        response = super().delete(request, *args, **kwargs)
        rmq.notify_contest_deleted(
            serializers.ContestSerializer(
                contest, display_sensitive_info=True,
            ).data,
        )
        return response


@extend_schema_view(
    post=extend_schema(
        tags=["Contest session"],
        responses={
            204: OpenApiResponse(
                description="Applied for contest",
            ),
            403: OpenApiResponse(
                description="Not allowed to apply, see error code",
                response=ErrorSerializer,
            ),
        },
    ),
)
class ApplyForContestView(APIView):
    """Make an application for contest."""

    serializer_class: BaseSerializer[Any] | None = None

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Make an application for contest."""
        contest_id = kwargs["contest_id"]
        contest = models.Contest.objects.get(id=contest_id)
        if not request.user.id:
            raise PermissionDenied(
                detail="You are not authorized to apply for contest",
                code="NOT_LOGGED_IN",
            )
        if not accessor.user_can_apply_for_contest(
            cast(User, request.user), contest,
        ):
            raise PermissionDenied(
                detail="You cannot apply for this contest",
                code="CANNOT_APPLY",
            )
        if accessor.user_applied_for_contest(request.user.id, contest):
            raise PermissionDenied(
                detail="You have already applied for this contest",
                code="ALREADY_APPLIED",
            )
        models.ContestSession.objects.create(
            user=request.user.id, contest=contest,
        )
        return Response(status=HTTPStatus.NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        tags=["Contest session"],
        responses={
            200: GetTimeSerializer,
            404: OpenApiResponse(
                description="Not found",
            ),
        },
    ),
)
class GetTimeLeft(APIView):
    """Get time user has to solve other tasks."""

    serializer_class = GetTimeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get time user has to solve other tasks."""
        contest = get_object_or_404(models.Contest, id=kwargs["contest_id"])
        time_left = accessor.user_get_time_left(request.user.id, contest)
        return Response(
            {
                "time_left": int(
                    time_left.total_seconds(),
                ) if time_left else -1,
                "is_unlimited": contest.time_limit_seconds < 0,
            },
        )


@extend_schema_view(
    get=extend_schema(
        tags=_CONTEST_MGMT_TAGS,
        responses={
            200: OpenApiResponse(
                description="List of (compiler id, syntax highlighting)",
                response=COMPILER_LIST_RESPONSE,
            ),
        },
    ),
)
class GetAvailableCompilersView(APIView):
    """List available compilers."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List available compilers."""
        return Response(settings.AVAILABLE_COMPILERS)


@extend_schema_view(
    get=extend_schema(
        tags=["Permissions"],
        responses={
            200: CanIManageContestSerializer,
        },
    ),
)
class CanIManageContestView(APIView):
    """Check if authenticated user can manage contest."""

    serializer_class = CanIManageContestSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Check if authenticated user can manage contest."""
        return Response(
            {
                "can_manage": models.Contest.objects.get(
                    id=kwargs["pk"],
                ).author == request.user.id,
            },
        )


@extend_schema_view(
    get=extend_schema(
        tags=["Contest session"],
        responses={
            200: OpenApiResponse(
                description="List of participant ids",
                response=PARTICIPANT_LIST_RESPONSE,
            ),
            404: OpenApiResponse(
                description="Not found",
            ),
        },
    ),
)
class GetContestParticipants(APIView):
    """Get list of users participating in contest."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get list of users participating in contest."""
        sessions = models.ContestSession.objects.filter(
            contest__id=kwargs["contest_id"],
        )
        return Response(
            [
                session.user
                for session in sessions
            ],
        )
