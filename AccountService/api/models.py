"""
ORM models
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


def get_default_user_settings() -> dict:
    """
    Default settings for user
    """
    return {}


def upload_pfp_to(instance, filename) -> str:
    # pylint: disable=unused-argument
    """Get path for profile picture"""
    return f"pfp/{uuid.uuid4()}.{filename.split('.')[-1]}"



class User(AbstractUser):
    """User model"""
    settings = models.JSONField(default=get_default_user_settings)
    profile_pic = models.ImageField(upload_to=upload_pfp_to, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_pic.name is None:
            return
        if len(self.profile_pic.name) < 1:
            return
        # pylint: disable=no-member
        image = Image.open(self.profile_pic.path)
        image.save(self.profile_pic.path, quality=20, optimize=True)


class IssuedToken(models.Model):
    """Model for invalidable JWT"""
    token = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(auto_now_add=True, blank=True)
    is_invalidated = models.BooleanField(default=False)
