from django.db import models


def purge_objects_of_user(user: int):
    QuizSolution.objects.filter(author=user).delete()
    CodeSolution.objects.filter(author=user).delete()


def purge_objects_of_quiz_task(task: int):
    QuizSolution.objects.filter(task_id=task).delete()


def purge_objects_of_code_task(task: int):
    CodeSolution.objects.filter(task_id=task).delete()


class QuizSolution(models.Model):
    author = models.IntegerField()
    task_id = models.IntegerField()
    points = models.IntegerField()
    is_solved = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class CodeSolution(models.Model):
    author = models.IntegerField()
    task_id = models.IntegerField()
    compiler = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)

    points = models.IntegerField(default=0)
    group_points = models.JSONField(default=dict)
    protocol = models.JSONField(blank=True, default=list)
    is_solved = models.BooleanField(default=False)
    verdict = models.CharField(default="NC")

    class SubmissionType(models.TextChoices):
        STRING = "str"
        ZIP = "zip"

    submission_type = models.CharField(max_length=3, choices=SubmissionType.choices)
    submission_data = models.TextField()

    class Status(models.TextChoices):
        NOT_CHECKED = "nc"
        IN_PROGRESS = "ip"
        CHECKED = "cc"
        INTERNAL_ERROR = "ie"

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.NOT_CHECKED)
