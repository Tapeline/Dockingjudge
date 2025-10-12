from datetime import datetime
from typing import override

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

from api.models import IssuedToken


class TokenWithInvalidation(AccessToken):
    """Token implementation."""

    @override
    def check_exp(
        self,
        claim: str = "exp",
        current_time: datetime | None = None,
    ) -> None:
        """Check if token is valid."""
        super().check_exp(claim, current_time)
        if (
            IssuedToken.objects.filter(token=str(self)).exists()
            and IssuedToken.objects.get(token=str(self)).is_invalidated
        ):
            raise InvalidToken(
                "Token invalidated",
                code="token_invalidated",
            )
