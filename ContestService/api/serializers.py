from rest_framework import serializers

from . import models


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contest
        fields = "__all__"
