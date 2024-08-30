import logging
from typing import Union

from django.db.models import Model
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models, accessor, permissions, validation, rmq


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
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


class RetrieveUpdateDestroyContestView(NotifyOnDeleteMixin,
                                       RetrieveUpdateDestroyAPIView):
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
            serializers.ContestSerializer(obj, display_sensitive_info=True).data
        )
        return response


class ListCreateTextPageView(ContestFieldInjectorOnCreation,
                             ListCreateAPIView):
    serializer_class = serializers.TextPageSerializer
    queryset = models.TextPage.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)


class RetrieveUpdateDestroyTextPageView(NotifyOnDeleteMixin,
                                        ContestFieldInjectorOnCreation,
                                        RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TextPageSerializer
    notification_serializer = serializer_class
    notify_function = rmq.notify_text_page_deleted
    queryset = models.TextPage.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)


class ListCreateQuizTaskView(ContestFieldInjectorOnCreation,
                             SerializerSwitchingMixin,
                             ListCreateAPIView,
                             ContestMixin):
    serializer_class = serializers.UserQuizTaskSerializer
    full_serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)


class RetrieveUpdateDestroyQuizTaskView(NotifyOnDeleteMixin,
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


class ListCreateCodeTaskView(ContestFieldInjectorOnCreation,
                             SerializerSwitchingMixin,
                             ListCreateAPIView,
                             ContestMixin):
    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)


class RetrieveUpdateDestroyCodeTaskView(NotifyOnDeleteMixin,
                                        ContestFieldInjectorOnCreation,
                                        SerializerSwitchingMixin,
                                        RetrieveUpdateDestroyAPIView,
                                        ContestMixin):
    serializer_class = serializers.UserCodeTaskSerializer
    full_serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()
    permission_classes = (IsAuthenticated,
                          permissions.IsContestAdminOrReadOnlyForParticipants)
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
            raise PermissionDenied(detail="You cannot apply for this contest", code="CANNOT_APPLY")
        models.ContestSession.objects.create(user=request.user.id, contest=contest)
        return Response(status=204)


class GetTimeLeft(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        contest = get_object_or_404(models.Contest, kwargs["contest_id"])
        return Response({
            "time_left": accessor.user_get_time_left(request.user.id, contest)
        })


class InternalRetrieveQuizTaskView(RetrieveAPIView):
    serializer_class = serializers.FullQuizTaskSerializer
    queryset = models.QuizTask.objects.all()


class InternalRetrieveCodeTaskView(RetrieveAPIView):
    serializer_class = serializers.FullCodeTaskSerializer
    queryset = models.CodeTask.objects.all()


