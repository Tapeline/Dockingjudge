import logging
from collections.abc import Callable
from http import HTTPStatus
from typing import Any

from django.db.models.base import Model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from api import accessor, models, permissions

# TODO: refactor to minimize mixin usage


class NotifyOnDeleteMixin[Model_T: Model]:
    """Sends a RMQ notification when object is deleted."""

    notification_serializer: type[BaseSerializer[Model_T]] | None = None
    notify_function: Callable[[dict[str, Any]], None] | None = None

    def delete(
        self: Any,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Call to delete and send notification."""
        if not self.notification_serializer or not self.notify_function:
            raise AssertionError(
                f"NotifyDeleteMixin misconfiguration: "
                f"{self.notification_serializer=}, {self.notify_function=}",
            )
        logger = logging.getLogger(self.__class__.__name__)
        deleting_obj = self.get_object()
        data = self.notification_serializer(deleting_obj).data
        response: Response = super().delete(request, *args, **kwargs)
        try:
            self.notify_function(data)
        except Exception:
            logger.exception(
                "Failed to notify deletion of %s", deleting_obj,
            )
        return response


class EnsureContestStructureIntegrityOnDeleteMixin:
    """Ensure contest pages list updates when page is deleted."""

    def delete(
        self: DestroyAPIView[models.Contest],
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Delete page and update contest."""
        page_task = self.get_object()
        page_type = None
        if isinstance(page_task, models.TextPage):
            page_type = "text"
        if isinstance(page_task, models.QuizTask):
            page_type = "quiz"
        if isinstance(page_task, models.CodeTask):
            page_type = "code"
        contest = page_task.contest
        contest.pages = [
            page
            for page in contest.pages
            if not (page["id"] == page_task.pk and page["type"] == page_type)
        ]
        contest.save()
        return super().delete(request, *args, **kwargs)


class EnsureContestStructureIntegrityOnCreateMixin:
    """Ensure contest pages list updates when page is created."""

    creating_page_type: str

    def contest_id_getter(self: APIView) -> int:
        """Get contest id."""
        return self.kwargs["contest_id"]

    def create(
        self: CreateAPIView[models.Contest],
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Create page and update contest."""
        response = super().create(request, *args, **kwargs)
        if response.status_code != HTTPStatus.CREATED:
            return response
        contest = models.Contest.objects.get(id=self.contest_id_getter())
        contest.pages = [
            *contest.pages,
            {"type": self.creating_page_type, "id": response.data["id"]},
        ]
        contest.save()
        return response


class ContestMixin:
    """Provides get_contest."""

    def get_contest(self: APIView) -> models.Contest:
        """Get referenced contest."""
        return accessor.get_object_or_null(
            models.Contest, id=self.kwargs.get("contest_id"),
        )


class SerializerSwitchingMixin:
    """Switches serializer to full when user can manage contest."""

    full_serializer_class = None

    def get_serializer_class(self: Any) -> type[BaseSerializer[Any]]:
        """Get serializer based on user permissions."""
        serializer_cls = super().get_serializer_class()
        if permissions.can_manage_contest(
            self.request.user.id, self.get_contest(),
        ):
            serializer_cls = self.full_serializer_class
        return serializer_cls


class ContestFieldInjectorOnCreation:
    """Add contest field to request data from path."""

    def create(
        self: CreateAPIView[Any],
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Add contest field and create."""
        request.data["contest"] = kwargs["contest_id"]
        return super().create(request, *args, **kwargs)
