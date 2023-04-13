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
        return self.username

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ["username"]


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=55, unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_genre_name")
        ]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    publication_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name="books")
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="books",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author", "publication_date"],
                name="unique_book",
            )
        ]
