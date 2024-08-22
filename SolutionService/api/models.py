from django.db import models


class Solution(models.Model):
    author = models.IntegerField()

    class TaskType(models.TextChoices):
        QUIZ = "quiz"
        CODE = "code"

    task_type = models.CharField(max_length=4, choices=TaskType.choices)
    task_id = models.IntegerField()
    protocol = models.JSONField(null=True, blank=True, default=None)
    points = models.IntegerField()
    group_points = models.JSONField(null=True, default=None)
    is_solved = models.BooleanField()
    text = models.TextField()
    verdict = models.CharField(default="NC")
    submitted_at = models.DateTimeField(auto_now_add=True)
    compiler = models.CharField(max_length=255, null=True, default=None)

    class Status(models.TextChoices):
        NOT_CHECKED = "nc"
        IN_PROGRESS = "ip"
        CHECKED = "cc"
        INTERNAL_ERROR = "ie"

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.NOT_CHECKED)
