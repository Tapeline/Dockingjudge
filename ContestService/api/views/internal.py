from typing import Any

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.generics import (
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, serializers


@extend_schema_view(
    get=extend_schema(
        tags=["Internal"],
        responses=serializers.FullQuizTaskSerializer,
    ),
)
class InternalRetrieveQuizTaskView(RetrieveAPIView[models.QuizTask]):
    """Get quiz task (with all sensitive data). Should not be exposed."""

    serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=["Internal"],
        responses=serializers.FullCodeTaskSerializer,
    ),
)
class InternalRetrieveCodeTaskView(RetrieveAPIView[models.CodeTask]):
    """Get code task (with all sensitive data). Should not be exposed."""

    serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=["Internal"],
        responses={
            200: OpenApiResponse(
                description=(
                    "List of code and quiz tasks (order is preserved). "
                    "For response spec see other internal endpoints."
                ),
                response=serializers.FullQuizTaskSerializer(many=True),
            ),
        },
    ),
)
class InternalGetAllTasksView(APIView):
    """Get list of all tasks (with sensitive data). Should not be exposed."""

    def get(  # noqa: WPS210
        self, request: Request, *args: Any, **kwargs: Any,
    ) -> Response:
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
        contest_pages = (
            (page["type"], page["id"]) for page in contest.pages
        )
        all_tasks = {"quiz": quiz_tasks, "code": code_tasks}
        return Response([
            {"type": page_type, **all_tasks[page_type][page_id]}
            for page_type, page_id in contest_pages
            if page_type in {"quiz", "code"}
        ])
