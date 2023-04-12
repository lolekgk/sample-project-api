from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    STUDENT = "S", _("Student")
    TEACHER = "T", _("Teacher")
