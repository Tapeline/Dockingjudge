from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, permissions, models, tasks, quiz_checker, rmq


class ListMyCodeSolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FullCodeSolutionSerializer
    queryset = models.CodeSolution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id)


class ListMyQuizSolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FullQuizSolutionSerializer
    queryset = models.QuizSolution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id)


class ListTaskCodeSolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CodeSolutionSerializer
    queryset = models.CodeSolution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            task_id=self.kwargs["task_id"],
            author=self.request.user.id
        )


class ListTaskQuizSolutionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.QuizSolutionSerializer
    queryset = models.QuizSolution.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            task_id=self.kwargs["task_id"],
            author=self.request.user.id
        )


class RetrieveCodeSolutionView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, permissions.IsOwnerOfThatSolution)
    serializer_class = serializers.FullCodeSolutionSerializer
    queryset = models.CodeSolution.objects.all()


class RetrieveQuizSolutionView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, permissions.IsOwnerOfThatSolution)
    serializer_class = serializers.FullQuizSolutionSerializer
    queryset = models.QuizSolution.objects.all()


class SubmitSolutionView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def _submit_quiz_answer(self, request, task: tasks.TaskMock):
        validator = quiz_checker.create_validator(task.data["validator"]["type"])
        is_correct = validator.validate(
            request.data["text"],
            task.data["validator"]["pattern"]
        )
        solution = models.QuizSolution(
            author=request.user.id,
            task_id=task.id,
            points=task.data["points"] if is_correct else 0,
            is_solved=is_correct,
            text=request.data["text"]
        )
        solution.save()
        return solution

    def _submit_code_answer(self, request, task: tasks.TaskMock):
        if not isinstance(request.data.get("compiler"), str):
            raise ValidationError("no field compiler", "NO_COMPILER")
        # TODO: add compiler validation
        if request.data.get("submission_type") not in ("str", "zip"):
            raise ValidationError("invalid submission type. only str and zip are supported",
                                  "INVALID_SUBMISSION_TYPE")
        if request.data.get("submission_type") == "zip":
            if len(request.data["text"].split(":")) != 2:
                raise ValidationError(
                    "invalid submission data. Expected base64:main_file",
                    "INVALID_SUBMISSION_DATA"
                )
        solution = models.CodeSolution(
            author=request.user.id,
            task_id=task.id,
            compiler=request.data["compiler"],
            submission_type=request.data["submission_type"],
            submission_data=request.data["text"]
        )
        solution.save()
        rmq.queue_code_solution(task, solution)
        solution.status = models.CodeSolution.Status.IN_PROGRESS
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
        if task.type == "quiz":
            solution = self._submit_quiz_answer(request, task)
            return Response(
                serializers.FullQuizSolutionSerializer(solution).data
            )
        elif task.type == "code":
            solution = self._submit_code_answer(request, task)
            return Response(
                serializers.FullCodeSolutionSerializer(solution).data
            )


def _get_user_score(self, user_id, task_type, task_id):
    model = {
        "code": models.CodeSolution,
        "quiz": models.QuizSolution
    }[task_type]
    solutions = model.objects.filter(author=user_id,
                                     task_id=int(task_id))
    if len(solutions) == 0:
        return None, None, False
    max_sol = solutions[0]
    for s in solutions:
        if s.points >= max_sol:
            max_sol = s
    return max_sol.id, max_sol.points, max_sol.is_solved


class GetTasksScoreForUserView(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        t = [task.split(":") for task in request.GET["tasks"]]
        return Response(
            [_get_user_score(self.kwargs["user_id"], *task) for task in t]
        )
