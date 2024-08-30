from rest_framework import serializers

from . import models


class CodeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeSolution
        fields = ("id", "task_type", "task_id", "points", "is_solved", "status",
                  "verdict", "group_points", "submitted_at", "compiler", "protocol")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for group in data["protocol"]:
            for i in range(len(group)):
                group[i] = {"verdict": group[i]["verdict"],
                            "is_successful": group[i]["is_successful"]}
        return data


class FullCodeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeSolution
        fields = "__all__"


class QuizSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizSolution
        fields = ("id", "task_id", "points", "submitted_at", "is_solved")


class FullQuizSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizSolution
        fields = "__all__"
