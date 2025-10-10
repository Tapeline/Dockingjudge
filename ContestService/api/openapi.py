from typing import Any, Final

from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    JSONField,
    ModelSerializer,
    Serializer,
)

from api import models

COMPILER_LIST_RESPONSE: Final = {  # noqa: WPS407
    "type": "array",
    "items": {
        "type": "array",
        "items": {
            "type": "string",
        },
        "minItems": 2,
        "maxItems": 2,
    },
}

PARTICIPANT_LIST_RESPONSE: Final = {  # noqa: WPS407
    "type": "array",
    "items": {
        "type": "integer",
    },
}


class ErrorSerializer(Serializer[Any]):
    """Generic error serializer."""

    detail = CharField(help_text="A message explaining the error.")
    code = CharField(help_text="A machine-readable error code.")


class GetTimeSerializer(Serializer[Any]):
    """Serializer for /time-left."""

    time_left = IntegerField(help_text="The time left in seconds.")
    is_unlimited = BooleanField(help_text="Is time unlimited.")


class CanIManageContestSerializer(Serializer[Any]):
    """Serializer for /can-manage."""

    can_manage = BooleanField(help_text="Can I manage this contest.")


class ContestCreationSerializer(ModelSerializer[models.Contest]):
    """Contest creation serializer."""

    class Meta:
        model = models.Contest
        fields = (
            "name", "description", "is_started", "is_ended",
            "time_limit_seconds",
        )


class ContestPatchSerializer(ModelSerializer[models.Contest]):
    """Contest patch serializer."""

    class Meta:
        model = models.Contest
        fields = (
            "name", "description", "is_started", "is_ended",
            "time_limit_seconds", "pages",
        )


class TextPageCreationSerializer(ModelSerializer[models.TextPage]):
    """Text page creation & patch serializer."""

    class Meta:
        model = models.TextPage
        fields = ("name", "text", "is_enter_page")


class QuizTaskCreationSerializer(ModelSerializer[models.QuizTask]):
    """Quiz task creation & patch serializer."""

    validator = JSONField(
        help_text=(
            "A validator description. "
            "See solution service doc for more details."
        ),
    )

    class Meta:
        model = models.QuizTask
        fields = ("title", "description", "validator", "points")


class CodeTaskCreationSerializer(ModelSerializer[models.CodeTask]):
    """Code task creation & patch serializer."""

    test_suite = JSONField(
        help_text=(
            "A test suite description. "
            "See solution service and judgelet doc for more details."
        ),
    )

    class Meta:
        model = models.CodeTask
        fields = ("title", "description", "test_suite")


class CanSubmitTaskSerializer(Serializer[Any]):
    """Serializer for /can-submit."""

    can_submit = BooleanField(help_text="Can a user submit this task.")
    reason = CharField(help_text="A reason for rejection.", required=False)
