from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import UserType


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=UserType.choices, max_length=1)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        default="default-profile-pic.png",
        upload_to="profile-pics/",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.username}"

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ["username"]
