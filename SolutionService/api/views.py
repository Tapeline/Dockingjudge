from django.shortcuts import render
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, permissions, models, tasks, quiz_checker, rmq


class ListMySolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FullSolutionSerializer
    queryset = models.Solution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id)


class ListTaskSolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SolutionSerializer
    queryset = models.Solution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            task_id=self.kwargs["task_id"],
            task_type=self.kwargs["task_type"]
        )


class RetrieveSolutionView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, permissions.IsOwnerOfThatSolution)
    serializer_class = serializers.FullSolutionSerializer
    queryset = models.Solution.objects.all()


class SubmitSolutionView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def _submit_quiz_answer(self, request, task: tasks.TaskMock):
        validator = quiz_checker.create_validator(task.data["validator"]["type"])
        is_correct = validator.validate(
            request.dsata["text"],
            task.data["validator"]["pattern"]
        )
        solution = models.Solution(
            author=request.user.id,
            task_type=task.type,
            task_id=task.id,
            points=task.data["points"] if is_correct else 0,
            is_solved=is_correct,
            text=request.data["text"],
            status=models.Solution.Status.CHECKED
        )
        solution.save()
        return solution

    def _submit_code_answer(self, request, task: tasks.TaskMock):
        if not isinstance(request.data.get("compiler"), str):
            raise ValidationError("no field compiler", "NO_COMPILER")
        solution = models.Solution(
            author=request.user.id,
            task_type=task.type,
            task_id=task.id,
            points=0,
            is_solved=False,
            text=request.data["text"],
            compiler=request.data["compiler"]
        )
        solution.save()
        rmq.queue_code_solution(task, solution)
        solution.status = models.Solution.Status.IN_PROGRESS
        solution.save()
        return solution

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data.get("text"), str):
            raise ValidationError("no field text", "NO_TEXT")
        response = tasks.can_sumbit(
            self.kwargs["task_type"],
            self.kwargs["task_id"],
            self.request.user.id
        )
        if not response["can_submit"]:
            return Response(response, status=403)
        task = tasks.get_task(self.kwargs["task_type"], self.kwargs["task_id"])
        if task is None:
            raise NotFound("task not found", "NO_SUCH_TASK")
        solution = None
        if task.type == "quiz":
            solution = self._submit_quiz_answer(request, task)
        elif task.type == "code":
            solution = self._submit_code_answer(request, task)
        return Response(
            serializers.FullSolutionSerializer(solution).data
        )
