from typing import Any, Final

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import accessor, models, permissions, rmq, serializers
from api.openapi import (
    CanSubmitTaskSerializer,
    CodeTaskCreationSerializer,
    QuizTaskCreationSerializer,
    TextPageCreationSerializer,
)
from api.views.mixins import (
    ContestFieldInjectorOnCreation,
    ContestMixin,
    EnsureContestStructureIntegrityOnCreateMixin,
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin,
    SerializerSwitchingMixin,
)

_PAGE_MGMT_TAGS: Final = ("Page & task management",)


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.TextPageSerializer(many=True),
    ),
    post=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=TextPageCreationSerializer,
        responses=serializers.TextPageSerializer,
    ),
)
class ListCreateTextPageView(
    EnsureContestStructureIntegrityOnCreateMixin,
    ContestFieldInjectorOnCreation,
    ListCreateAPIView[models.TextPage],
):
    """List or create text pages."""

    serializer_class = serializers.TextPageSerializer
    queryset = models.TextPage.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    creating_page_type = "text"


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.TextPageSerializer,
    ),
    patch=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=TextPageCreationSerializer,
        responses=serializers.TextPageSerializer,
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=_PAGE_MGMT_TAGS,
    ),
)
class RetrieveUpdateDestroyTextPageView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin[models.TextPage],
    ContestFieldInjectorOnCreation,
    RetrieveUpdateDestroyAPIView[models.TextPage],
):
    """Get, update or delete a single text page."""

    serializer_class = serializers.TextPageSerializer
    notification_serializer = serializer_class
    notify_function = rmq.notify_text_page_deleted  # type: ignore[assignment]
    queryset = models.TextPage.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.UserQuizTaskSerializer(many=True),
    ),
    post=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=QuizTaskCreationSerializer,
        responses=serializers.FullQuizTaskSerializer,
    ),
)
class ListCreateQuizTaskView(
    EnsureContestStructureIntegrityOnCreateMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    ListCreateAPIView[models.QuizTask],
    ContestMixin,
):
    """
    List or create quiz tasks.

    If you are a contest manager, additional info is exposed.

    """

    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    creating_page_type = "quiz"


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.UserQuizTaskSerializer,
    ),
    patch=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=QuizTaskCreationSerializer,
        responses=serializers.FullQuizTaskSerializer,
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=_PAGE_MGMT_TAGS,
    ),
)
class RetrieveUpdateDestroyQuizTaskView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin[models.QuizTask],
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    RetrieveUpdateDestroyAPIView[models.QuizTask],
    ContestMixin,
):
    """
    Get, update or delete a single quiz task.

    If you are a contest manager, additional info is exposed.

    """

    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_quiz_task_deleted  # type: ignore[assignment]


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.UserCodeTaskSerializer(many=True),
    ),
    post=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=CodeTaskCreationSerializer,
        responses=serializers.FullCodeTaskSerializer,
    ),
)
class ListCreateCodeTaskView(
    EnsureContestStructureIntegrityOnCreateMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    ListCreateAPIView[models.CodeTask],
    ContestMixin,
):
    """
    List or create code tasks.

    If you are a contest manager, additional info is exposed.

    """

    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    creating_page_type = "code"


@extend_schema_view(
    get=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        responses=serializers.UserCodeTaskSerializer,
    ),
    patch=extend_schema(
        tags=_PAGE_MGMT_TAGS,
        request=CodeTaskCreationSerializer,
        responses=serializers.FullCodeTaskSerializer,
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=_PAGE_MGMT_TAGS,
    ),
)
class RetrieveUpdateDestroyCodeTaskView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin[models.CodeTask],
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    RetrieveUpdateDestroyAPIView[models.CodeTask],
    ContestMixin,
):
    """
    Get, update or delete a single code task.

    If you are a contest manager, additional info is exposed.

    """

    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_code_task_deleted  # type: ignore[assignment]


@extend_schema_view(
    get=extend_schema(
        tags=["Permissions"],
        responses=CanSubmitTaskSerializer,
    ),
)
class CanSubmitSolutionToTask(APIView):
    """Check if a user can submit solution to specific task."""

    serializer_class = CanSubmitTaskSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Check if a user can submit solution to specific task."""
        user = kwargs["user_id"]
        task_type = kwargs["task_type"]
        task_id = kwargs["task_id"]
        task = validate_task_id_and_get(task_type, task_id)
        if not accessor.user_applied_for_contest(user, task.contest):
            return Response(
                {
                    "can_submit": False,
                    "reason": "NOT_REGISTERED",
                },
            )
        if (
            not accessor.user_has_time_left(user, task.contest)
            or not accessor.is_contest_open(task.contest)
        ):
            return Response(
                {
                    "can_submit": False,
                    "reason": "CONTEST_ENDED",
                },
            )
        return Response(
            {
                "can_submit": True,
            },
        )


def validate_task_id_and_get(
    task_type: str, task_id: int,
) -> models.QuizTask | models.CodeTask:
    """Try to get task of given type and id."""
    if task_type not in ("quiz", "code"):
        raise ValidationError(
            f"Bad task type {task_type}",
            "BAD_TASK_TYPE",
        )
    model = {
        "quiz": models.QuizTask,
        "code": models.CodeTask,
    }[task_type]
    if not model.objects.filter(  # type: ignore[attr-defined]
        id=task_id,
    ).exists():
        raise ValidationError(
            f"No task of type {task_type} with id {task_id}", "NOT_FOUND",
        )
    return model.objects.get(  # type: ignore[attr-defined,no-any-return]
        id=task_id,
    )
