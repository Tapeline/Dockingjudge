from rest_framework import serializers
from rest_framework.fields import empty

from . import models


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contest
        fields = "__all__"

    def __init__(self, instance=None, data=empty,
                 display_only_enter_pages=False,
                 display_sensitive_info=False,
                 **kwargs):
        super().__init__(instance, data, **kwargs)
        self.display_only_enter_pages = display_only_enter_pages
        self.display_sensitive_info = display_sensitive_info

    def _get_page_repr(self, page_type, page_id):
        model = {
            "text": models.TextPage,
            "quiz": models.QuizTask,
            "code": models.CodeTask
        }[page_type]
        serializer = {
            "text": TextPageSerializer,
            "quiz": UserQuizTaskSerializer if not self.display_sensitive_info
            else FullQuizTaskSerializer,
            "code": UserCodeTaskSerializer if not self.display_sensitive_info
            else FullCodeTaskSerializer,
        }[page_type]
        return serializer(model.objects.get(id=page_id)).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for page in data["pages"]:
            page["content"] = self._get_page_repr(page["type"], page["id"])
        if self.display_only_enter_pages:
            data["pages"] = [
                page for page in data["pages"]
                if page["content"].get("is_enter_page") is True
            ]
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
        fields = ["contest", "title", "description", "points"]


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
        if "precompile" in suite:
            del suite["precompile"]
        if "place_files" in suite:
            del suite["place_files"]
        data["max_points"] = sum(group["points"] for group in suite["groups"])
        for group in suite["groups"]:
            group["cases"] = len(group["cases"])
        data["test_suite"] = suite
        return data
