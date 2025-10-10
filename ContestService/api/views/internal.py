from typing import Any

from rest_framework.generics import (
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, serializers


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
