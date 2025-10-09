import logging
from typing import Union, Callable

import requests
from django.db.models import Model
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models, accessor, permissions, validation, rmq
from contest_service import settings


class NotifyOnDeleteMixin:
    notification_serializer = None
    notify_function = None

    def delete(self, request, *args, **kwargs):
        obj: Model = self.get_object()
        data = self.notification_serializer(obj).data
        response = super().delete(request, *args, **kwargs)
        try:
            self.notify_function(data)
        except Exception as e:
            logging.error("Failed to notify deletion of %s: %s", obj, e)
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
        contest.pages = contest.pages + [{"type": self.creating_page_type, "id": response.data["id"]}]
        contest.save()
        return response


class ContestMixin:
    def get_contest(self):
        return accessor.get_object_or_null(models.Contest, id=self.kwargs.get("contest_id"))


class SerializerSwitchingMixin:
    full_serializer_class = None

    def get_serializer_class(self):
        cls = super().get_serializer_class()
        if permissions.can_manage_contest(self.request.user.id, self.get_contest()):
            cls = self.full_serializer_class
        return cls


class ContestFieldInjectorOnCreation:
    def create(self, request, *args, **kwargs):
        request.data["contest"] = kwargs["contest_id"]
        return super().create(request, *args, **kwargs)


class ListCreateContestView(ListCreateAPIView):
    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (IsAuthenticated, permissions.CanCreateContest)

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


class RetrieveUpdateDestroyContestView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnly)

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(
            *args, **kwargs,
            display_only_enter_pages=not permissions.can_view_all_pages(
                self.request.user.id, self.get_object()
            ),
            display_sensitive_info=permissions.can_manage_contest(
                self.request.user.id, self.get_object()
            )
        )

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        rmq.notify_contest_deleted(
            serializers.ContestSerializer(
                obj, display_sensitive_info=True
            ).data
        )
        return response


class ListCreateTextPageView(EnsureContestStructureIntegrityOnCreateMixin,
                             ContestFieldInjectorOnCreation,
                             ListCreateAPIView):
    serializer_class = serializers.TextPageSerializer
    queryset = models.TextPage.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)
    creating_page_type = "text"


class RetrieveUpdateDestroyTextPageView(EnsureContestStructureIntegrityOnDeleteMixin,
                                        NotifyOnDeleteMixin,
                                        ContestFieldInjectorOnCreation,
                                        RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TextPageSerializer
    notification_serializer = serializer_class
    notify_function = rmq.notify_text_page_deleted
    queryset = models.TextPage.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)


class ListCreateQuizTaskView(EnsureContestStructureIntegrityOnCreateMixin,
                             ContestFieldInjectorOnCreation,
                             SerializerSwitchingMixin,
                             ListCreateAPIView,
                             ContestMixin):
    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)
    creating_page_type = "quiz"


class RetrieveUpdateDestroyQuizTaskView(EnsureContestStructureIntegrityOnDeleteMixin,
                                        NotifyOnDeleteMixin,
                                        ContestFieldInjectorOnCreation,
                                        SerializerSwitchingMixin,
                                        RetrieveUpdateDestroyAPIView,
                                        ContestMixin):
    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_quiz_task_deleted


class ListCreateCodeTaskView(EnsureContestStructureIntegrityOnCreateMixin,
                             ContestFieldInjectorOnCreation,
                             SerializerSwitchingMixin,
                             ListCreateAPIView,
                             ContestMixin):
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
    RetrieveUpdateDestroyAPIView,
    ContestMixin
):
    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsContestAdminOrReadOnlyForParticipants
    )
    notification_serializer = full_serializer_class
    notify_function = rmq.notify_code_task_deleted


class CanSubmitSolutionToTask(APIView):
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user_id")
        task_type = kwargs.get("task_type")
        task_id = kwargs.get("task_id")
        task = validation.validate_task_id_and_get(task_type, task_id)
        task: models.CodeTask | models.QuizTask
        if not accessor.user_applied_for_contest(user, task.contest):
            return Response({
                "can_submit": False,
                "reason": "NOT_REGISTERED"
            })
        if not accessor.user_has_time_left(user, task.contest):
            return Response({
                "can_submit": False,
                "reason": "CONTEST_ENDED"
            })
        if not accessor.is_contest_open(task.contest):
            return Response({
                "can_submit": False,
                "reason": "CONTEST_ENDED"
            })
        return Response({
            "can_submit": True
        })


class ApplyForContestView(APIView):
    def post(self, request, *args, **kwargs):
        contest_id = kwargs.get("contest_id")
        contest = models.Contest.objects.get(id=contest_id)
        if not accessor.user_can_apply_for_contest(request.user, contest):
            raise PermissionDenied(detail="You cannot apply for this contest",
                                   code="CANNOT_APPLY")
        if accessor.user_applied_for_contest(request.user.id, contest):
            raise PermissionDenied(detail="You have already applied for this contest",
                                   code="ALREADY_APPLIED")
        models.ContestSession.objects.create(user=request.user.id, contest=contest)
        return Response(status=204)


class GetTimeLeft(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        contest = get_object_or_404(models.Contest, id=kwargs["contest_id"])
        return Response({
            "time_left": int((
                accessor.user_get_time_left(request.user.id, contest)
            ).total_seconds()),
            "is_unlimited": contest.time_limit_seconds < 0
        })


class GetAvailableCompilersView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(settings.AVAILABLE_COMPILERS)


class CanIManageContestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "can_manage": models.Contest.objects.get(id=kwargs["pk"]).author == request.user.id
        })


class GetContestParticipants(APIView):
    def get(self, request, *args, **kwargs):
        sessions = models.ContestSession.objects.filter(
            contest__id=kwargs["contest_id"])
        return Response([
            session.user
            for session in sessions
        ])


class InternalRetrieveQuizTaskView(RetrieveAPIView):
    serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()


class InternalRetrieveCodeTaskView(RetrieveAPIView):
    serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()


class InternalGetAllTasksView(APIView):
    def get(self, request, *args, **kwargs):
        quiz_tasks = models.QuizTask.objects.filter(contest__id=kwargs["contest_id"])
        code_tasks = models.CodeTask.objects.filter(contest__id=kwargs["contest_id"])
        quiz_tasks = [
            {"type": "quiz", **serializers.FullQuizTaskSerializer(t).data}
            for t in quiz_tasks
        ]
        code_tasks = [
            {"type": "code", **serializers.FullCodeTaskSerializer(t).data}
            for t in code_tasks
        ]
        return Response(quiz_tasks + code_tasks)
