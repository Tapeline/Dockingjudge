from django.db import models

from . import validation


def purge_objects_of_user(user: int):
    Contest.objects.filter(author=user).delete()
    ContestSession.objects.filter(user=user).delete()


class Contest(models.Model):
    name = models.CharField(max_length=255)
    author = models.IntegerField()
    description = models.TextField()
    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    time_limit_seconds = models.IntegerField(default=-1)
    pages = models.JSONField(default=list)

    def save(self, **kwargs):
        validation.validate_pages_list(self.pages)
        super().save(**kwargs)


class ContestSession(models.Model):
    user = models.IntegerField()
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)


class TextPage(models.Model):
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text = models.TextField()
    is_enter_page = models.BooleanField(default=False)


class CodeTask(models.Model):
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    test_suite = models.JSONField()

    def save(self, **kwargs):
        validation.validate_test_suite(self.test_suite)
        super().save(**kwargs)


class QuizTask(models.Model):
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    validator = models.JSONField(default=dict)
    points = models.IntegerField()

    def save(self, **kwargs):
        validation.validate_quiz_validator(self.validator)
        super().save(**kwargs)
