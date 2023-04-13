from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    REGULAR = "R", _("Regular")
    PREMIUM = "P", _("Premium")
