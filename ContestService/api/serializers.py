from rest_framework import serializers
from rest_framework.fields import empty

from . import models


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contest
        fields = "__all__"

    def __init__(self, instance=None, data=empty,
                 display_only_enter_pages=False, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.display_only_enter_pages = display_only_enter_pages

    def _get_page_repr(self, page_type, page_id):
        model = {
            "text": models.TextPage,
            "quiz": models.QuizTask,
            "code": models.CodeTask
        }[page_type]
        serializer = {
            "text": TextPageSerializer,
            "quiz": UserQuizTaskSerializer,
            "code": UserCodeTaskSerializer
        }[page_type]
        return serializer(model.object.get(id=page_id)).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.display_only_enter_pages:
            return data
        data["pages"] = [
            page for page in data["pages"]
            if page.get("is_enter_page") is True
        ]
        for page in data["pages"]:
            page["content"] = self._get_page_repr(page["type"], page["id"])
        return data


class TextPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextPage
        fields = "__all__"


class FullQuizTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizTask
        fields = "__all__"


class UserQuizTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizTask
        fields = ["contest", "title", "description"]


class FullCodeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeTask
        fields = "__all__"


class UserCodeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeTask
        fields = ["contest", "title", "description", "test_suite"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        suite = data["test_suite"]
        data["max_points"] = sum(group["points"] for group in suite)
        for group in suite:
            group["cases"] = len(group["cases"])
        data["test_suite"] = suite
        return data
