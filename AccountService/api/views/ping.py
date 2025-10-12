from urllib.request import Request

from django.http.response import HttpResponse
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework.views import APIView


@extend_schema_view(
    get=extend_schema(
        responses={
            200: {
                "description": "Service alive.",
            },
        },
    ),
)
class PingView(APIView):
    """Ping."""

    def get(self, _: Request) -> HttpResponse:
        """Ping."""
        return HttpResponse("ok", content_type="text/plain")
