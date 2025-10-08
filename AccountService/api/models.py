import uuid
from typing import Any, Final, override

from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

_PFP_QUALITY_COEFF: Final = 20


def get_default_user_settings() -> dict[str, Any]:
    """Default settings for user."""
    return {}


def upload_pfp_to(_: Any, filename: str) -> str:
    """Get path for profile picture."""
    extension = filename.split(".")[-1]
    return f"pfp/{uuid.uuid4()}.{extension}"


class User(AbstractUser):
    """User model."""

    settings = models.JSONField(default=get_default_user_settings)
    profile_pic = models.ImageField(
        upload_to=upload_pfp_to, blank=True, null=True,
    )

    @override
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the user and its pfp."""
        super().save(*args, **kwargs)
        if self.profile_pic.name is None:
            return
        if len(self.profile_pic.name) < 1:
            return
        image = Image.open(self.profile_pic.path)
        image.save(
            self.profile_pic.path, quality=_PFP_QUALITY_COEFF, optimize=True,
        )


class IssuedToken(models.Model):
    """Model for invalidable JWT."""

    token = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(auto_now_add=True, blank=True)
    is_invalidated = models.BooleanField(default=False)
