from urllib.request import Request

from django.http.response import HttpResponse
from rest_framework.views import APIView


class PingView(APIView):
    """Ping."""

    def get(self, _: Request) -> HttpResponse:
        """Ping."""
        return HttpResponse("ok", content_type="text/plain")
