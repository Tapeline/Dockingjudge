from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers, models


class ListCreateContestViews(ListCreateAPIView):
    serializer_class = serializers.ContestSerializer
    queryset = models.Contest.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)
