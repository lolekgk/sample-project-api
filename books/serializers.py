from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import (
    UserDetailsSerializer as BaseUserDetailsSerializer,
)
from django.contrib.auth import get_user_model
from drf_writable_nested.mixins import NestedCreateMixin
from rest_framework import serializers

from .constants import UserType
from .models import Author, Book, Genre

UserModel = get_user_model()


class RegisterSerializer(BaseRegisterSerializer):
    user_type = serializers.CharField(required=True)

    def validate_user_type(self, value):
        try:
            UserType(value)
        except ValueError:
            raise serializers.ValidationError("Invalid user type")
        return value

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data["user_type"] = self.validated_data.get("user_type", "")
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.user_type = self.cleaned_data.get("user_type", "")
        user.save()
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]


class GenreSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "email",
            "user_type",
            "password",
        ]


class BookListCreateSerializer(NestedCreateMixin, serializers.ModelSerializer):
    genres = GenreSeralizer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = [
            "pk",
            "title",
            "author",
            "genres",
            "publication_date",
            "owner",
        ]


class BookUpdateSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True
    )
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = [
            "pk",
            "title",
            "author",
            "genres",
            "publication_date",
            "owner",
        ]


class UserDetailsSerializer(BaseUserDetailsSerializer):
    class Meta:
        model = UserModel
        extra_fields = []

        if hasattr(UserModel, "USERNAME_FIELD"):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, "EMAIL_FIELD"):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, "first_name"):
            extra_fields.append("first_name")
        if hasattr(UserModel, "last_name"):
            extra_fields.append("last_name")
        if hasattr(UserModel, "user_type"):
            extra_fields.append("user_type")

        fields = ("pk", *extra_fields)
        read_only_fields = ("email",)
