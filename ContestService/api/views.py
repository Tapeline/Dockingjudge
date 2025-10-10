import logging
from typing import Any

from django.db.models import Model
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from api import accessor, models, permissions, rmq, serializers, validation
from contest_service import settings


class NotifyOnDeleteMixin:
    """Sends a RMQ notification when object is deleted."""

    notification_serializer = None
    notify_function = None

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        obj: Model = self.get_object()
        data = self.notification_serializer(obj).data
        response = super().delete(request, *args, **kwargs)
        try:
            self.notify_function(data)
        except Exception as e:
            logging.exception("Failed to notify deletion of %s: %s", obj, e)
        return response


class EnsureContestStructureIntegrityOnDeleteMixin:
    def delete(self, request, *args, **kwargs):
        obj: Model = self.get_object()
        page_type = None
        if isinstance(obj, models.TextPage):
            page_type = "text"
        if isinstance(obj, models.QuizTask):
            page_type = "quiz"
        if isinstance(obj, models.CodeTask):
            page_type = "code"
        contest = obj.contest
        contest.pages = [
            page
            for page in contest.pages
            if not (page["id"] == obj.id and page["type"] == page_type)
        ]
        contest.save()
        return super().delete(request, *args, **kwargs)


class EnsureContestStructureIntegrityOnCreateMixin:
    creating_page_type: str

    def contest_id_getter(self):
        return self.kwargs["contest_id"]

    def create(self, request, *args, **kwargs):
        response: Response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
            return response
        contest = models.Contest.objects.get(id=self.contest_id_getter())
        contest.pages = contest.pages + [
            {"type": self.creating_page_type, "id": response.data["id"]}]
        contest.save()
        return response


class ContestMixin:
    def get_contest(self):
        return accessor.get_object_or_null(
            models.Contest, id=self.kwargs.get("contest_id"),
        )


class SerializerSwitchingMixin:
    full_serializer_class = None

    def get_serializer_class(self):
        cls = super().get_serializer_class()
        if permissions.can_manage_contest(
            self.request.user.id, self.get_contest(),
        ):
            cls = self.full_serializer_class
        return cls


class ContestFieldInjectorOnCreation:
    def create(self, request, *args, **kwargs):
        request.data["contest"] = kwargs["contest_id"]
        return super().create(request, *args, **kwargs)


class ListCreateContestView(ListCreateAPIView[models.Contest]):
    """Get all contests or create new one."""

    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (IsAuthenticated, permissions.CanCreateContest)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create contest, author field is injected automatically."""
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


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


class RetrieveUpdateDestroyTextPageView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin,
    ContestFieldInjectorOnCreation,
    RetrieveUpdateDestroyAPIView[models.TextPage],
):
    """Get, update or delete a single text page."""

    serializer_class = serializers.TextPageSerializer
    notification_serializer = serializer_class
    notify_function = rmq.notify_text_page_deleted
    queryset = models.TextPage.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )


class ListCreateQuizTaskView(
    EnsureContestStructureIntegrityOnCreateMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    ListCreateAPIView[models.QuizTask],
    ContestMixin,
):
    """List or create quiz tasks."""

    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (IsAuthenticated,
    permissions.IsContestAdminOrReadOnlyForParticipants)
    creating_page_type = "quiz"


class RetrieveUpdateDestroyQuizTaskView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    RetrieveUpdateDestroyAPIView[models.QuizTask],
    ContestMixin,
):
    """Get, update or delete a single quiz task."""

    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (IsAuthenticated,
    permissions.IsContestAdminOrReadOnlyForParticipants)
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_quiz_task_deleted


class ListCreateCodeTaskView(
    EnsureContestStructureIntegrityOnCreateMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    ListCreateAPIView[models.CodeTask],
    ContestMixin,
):
    """List or create code tasks."""

    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (IsAuthenticated,
    permissions.IsContestAdminOrReadOnlyForParticipants)
    creating_page_type = "code"


class RetrieveUpdateDestroyCodeTaskView(
    EnsureContestStructureIntegrityOnDeleteMixin,
    NotifyOnDeleteMixin,
    ContestFieldInjectorOnCreation,
    SerializerSwitchingMixin,
    RetrieveUpdateDestroyAPIView[models.CodeTask],
    ContestMixin,
):
    """Get, update or delete a single code task."""

    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants,
    )
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_code_task_deleted


class CanSubmitSolutionToTask(APIView):
    """Check if a user can submit solution to specific task."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Check if a user can submit solution to specific task."""
        user = kwargs.get("user_id")
        task_type = kwargs.get("task_type")
        task_id = kwargs.get("task_id")
        task = validation.validate_task_id_and_get(task_type, task_id)
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


class ApplyForContestView(APIView):
    """Make an application for contest."""

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Make an application for contest."""
        contest_id = kwargs.get("contest_id")
        contest = models.Contest.objects.get(id=contest_id)
        if not accessor.user_can_apply_for_contest(request.user, contest):
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
        return Response(status=204)


class GetTimeLeft(APIView):
    """Get time user has to solve other tasks."""

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get time user has to solve other tasks."""
        contest = get_object_or_404(models.Contest, id=kwargs["contest_id"])
        return Response(
            {
                "time_left": int(
                    accessor.user_get_time_left(
                        request.user.id, contest,
                    ).total_seconds(),
                ),
                "is_unlimited": contest.time_limit_seconds < 0,
            },
        )


class GetAvailableCompilersView(APIView):
    """List available compilers."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List available compilers."""
        return Response(settings.AVAILABLE_COMPILERS)


class CanIManageContestView(APIView):
    """Check if authenticated user can manage contest."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Check if authenticated user can manage contest."""
        return Response(
            {
                "can_manage": models.Contest.objects.get(
                    id=kwargs["pk"],
                ).author == request.user.id,
            },
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


class InternalRetrieveQuizTaskView(RetrieveAPIView):
    """Get quiz task (with all sensitive data). Should not be exposed."""

    serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()


class InternalRetrieveCodeTaskView(RetrieveAPIView):
    """Get code task (with all sensitive data). Should not be exposed."""

    serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()


class InternalGetAllTasksView(APIView):
    """Get list of all tasks (with sensitive data). Should not be exposed."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get list of all tasks (with sensitive data). Do not expose."""
        contest = get_object_or_404(models.Contest, id=kwargs["contest_id"])
        quiz_tasks = {
            task.pk: serializers.FullQuizTaskSerializer(task).data
            for task in models.QuizTask.objects.filter(
                contest__id=kwargs["contest_id"],
            )
        }
        code_tasks = {
            task.pk: serializers.FullCodeTaskSerializer(task).data
            for task in models.CodeTask.objects.filter(
                contest__id=kwargs["contest_id"],
            )
        }
        all_tasks = {"quiz": quiz_tasks, "code": code_tasks}
        return Response([
            {"type": page["type"], **all_tasks[page["type"]][page["id"]]}
            for page in contest.pages
            if page["type"] in {"quiz", "code"}
        ])


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
    if not model.objects.filter(id=task_id).exists():
        raise ValidationError(
            f"No task of type {task_type} with id {task_id}", "NOT_FOUND",
        )
    return model.objects.get(id=task_id)
