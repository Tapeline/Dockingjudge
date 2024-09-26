"""
Provides mechanisms for validating tokens that may be invalidated
"""

from datetime import datetime
from typing import Optional

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

from .models import IssuedToken


class TokenWithInvalidation(AccessToken):
    """Token implementation"""
    def check_exp(self, claim: str = "exp",
                  current_time: Optional[datetime] = None) -> None:
        """Check if token is valid"""
        # pylint: disable=no-member
        super().check_exp(claim, current_time)
        if IssuedToken.objects.filter(token=str(self)).exists() and \
                IssuedToken.objects.get(token=str(self)).is_invalidated:
            raise InvalidToken("Token invalidated", code="token_invalidated")
