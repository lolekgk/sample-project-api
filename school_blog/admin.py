from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import F
from django.http import HttpRequest

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "full_name",
        "age",
        "profile_picture",
        "is_staff",
    ]
    list_editable = ["profile_picture", "is_staff"]
    list_per_page = 10
    list_filter = [
        "date_joined",
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    ]
    ordering = ["first_name", "last_name"]
    search_fields = [
        "first_name__istartswith",
        "last_name__istartswith",
        "email__istartswith",
    ]

    # fields in 'edit' panel
    fieldsets = (
        ("Sign-in data", {"fields": ("username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "birth_date",
                    "profile_picture",
                    "user_type",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # fields in 'add' panel
    add_fieldsets = (
        (
            (None),
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "birth_date",
                    "profile_picture",
                ),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest):
        return (
            super()
            .get_queryset(request)
            .annotate(
                age=datetime.now().year - F("birth_date__year"),
            )
        )

    @admin.display(ordering="age")
    def age(self, user: User):
        return user.age

    @admin.display(ordering="full_name")
    def full_name(self, user: User):
        return user.get_full_name()
