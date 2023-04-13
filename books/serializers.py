from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import (
    UserDetailsSerializer as BaseUserDetailsSerializer,
)
from django.contrib.auth import get_user_model
from drf_writable_nested.mixins import (
    NestedCreateMixin,
    NestedUpdateMixin,
    UniqueFieldsMixin,
)
from rest_framework import serializers

from .constants import UserType
from .models import Author, Book, Genre

UserModel = get_user_model()


class AuthorSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "id_number"]


class GenreSeralizer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


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

    def validate(self, data):
        author_data = data.get("author")
        title = data.get("title")
        publication_date = data.get("publication_date")

        author = Author.objects.filter(
            id_number=author_data["id_number"]
        ).first()
        if (
            author
            and Book.objects.filter(
                title=title, author=author, publication_date=publication_date
            ).exists()
        ):
            raise serializers.ValidationError(
                "This book already exists in the database."
            )
        return data

    def create_author(self, author_data):
        author, _ = Author.objects.get_or_create(
            id_number=author_data["id_number"],
            defaults={
                "first_name": author_data["first_name"],
                "last_name": author_data["last_name"],
            },
        )
        return author

    def create_genres(self, genres_data):
        genres = []
        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
            genres.append(genre)
        return genres

    def create(self, validated_data):
        author_data = validated_data.pop("author")
        genres_data = validated_data.pop("genres")

        author = self.create_author(author_data)
        genres = self.create_genres(genres_data)

        book = Book.objects.create(
            title=validated_data["title"],
            author=author,
            publication_date=validated_data["publication_date"],
            owner=validated_data["owner"],
        )
        book.genres.set(genres)

        return book


class BookUpdateSerializer(NestedUpdateMixin, serializers.ModelSerializer):
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

    def create_or_update_author(self, author_data):
        author, _ = Author.objects.get_or_create(**author_data)
        return author

    def create_or_update_genres(self, genres_data):
        genres = []
        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
            genres.append(genre)
        return genres

    def update(self, instance, validated_data):
        author_data = validated_data.pop("author", None)
        genres_data = validated_data.pop("genres", [])

        if author_data:
            author = self.create_or_update_author(author_data)
            instance.author = author

        if genres_data:
            genres = self.create_or_update_genres(genres_data)
            instance.genres.set(genres)

        return super().update(instance, validated_data)


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
