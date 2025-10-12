from typing import Any, override

from rest_framework import serializers
from rest_framework.fields import empty

from api import models


class ContestSerializer(serializers.ModelSerializer[models.Contest]):
    """Serializer for Contest objects."""

    class Meta:
        model = models.Contest
        fields = "__all__"

    def __init__(
        self,
        instance: Any = None,
        data: Any = empty,
        *,
        display_only_enter_pages: bool = False,
        display_sensitive_info: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(instance, data, **kwargs)
        self.display_only_enter_pages = display_only_enter_pages
        self.display_sensitive_info = display_sensitive_info

    @override
    def to_representation(self, instance: models.Contest) -> Any:
        data = super().to_representation(instance)
        for content_page in data["pages"]:
            content_page["content"] = self._get_page_repr(
                content_page["type"], content_page["id"],
            )
        if self.display_only_enter_pages:
            data["pages"] = [
                page for page in data["pages"]
                if page["content"].get("is_enter_page") is True
            ]
        return data

    def _get_page_repr(self, page_type: str, page_id: int) -> Any:
        """Serialize a single page."""
        model = {
            "text": models.TextPage,
            "quiz": models.QuizTask,
            "code": models.CodeTask,
        }[page_type]
        serializer = {
            "text": TextPageSerializer,
            "quiz": FullQuizTaskSerializer if self.display_sensitive_info
            else UserQuizTaskSerializer,
            "code": FullCodeTaskSerializer if self.display_sensitive_info
            else UserCodeTaskSerializer,
        }[page_type]
        return serializer(
            model.objects.get(id=page_id),  # type: ignore[attr-defined]
        ).data


class TextPageSerializer(serializers.ModelSerializer[models.TextPage]):
    """Serializer for TextPage objects."""

    class Meta:
        model = models.TextPage
        fields = "__all__"


class FullQuizTaskSerializer(serializers.ModelSerializer[models.QuizTask]):
    """Serializer for QuizTask objects with sensitive info."""

    class Meta:
        model = models.QuizTask
        fields = "__all__"


class UserQuizTaskSerializer(serializers.ModelSerializer[models.QuizTask]):
    """Serializer for QuizTask objects that hides sensitive info."""

    class Meta:
        model = models.QuizTask
        fields = ("contest", "title", "description", "points")


class FullCodeTaskSerializer(serializers.ModelSerializer[models.CodeTask]):
    """Serializer for Code objects with sensitive info."""

    class Meta:
        model = models.CodeTask
        fields = "__all__"


class UserCodeTaskSerializer(serializers.ModelSerializer[models.CodeTask]):
    """Serializer for CodeTask objects that hides sensitive info."""

    class Meta:
        model = models.CodeTask
        fields = ("contest", "title", "description", "test_suite")

    @override
    def to_representation(self, instance: models.CodeTask) -> Any:
        data = super().to_representation(instance)
        suite = data["test_suite"]
        if "precompile" in suite:
            suite.pop("precompile")
        if "place_files" in suite:
            suite.pop("place_files")
        data["max_points"] = sum(group["points"] for group in suite["groups"])
        for group in suite["groups"]:
            group["cases"] = len(group["cases"])
        data["test_suite"] = suite
        return data
