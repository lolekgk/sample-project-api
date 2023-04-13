from django.urls import path

from .views import BookCreateView, BookListView, BookUpdateView

app_name = "books"


urlpatterns = [
    path(
        "",
        BookListView.as_view(),
        name="book_list",
    ),
    path(
        "<int:pk>/",
        BookUpdateView.as_view(),
        name="book_update_as_owner",
    ),
    path(
        "create_record/",
        BookCreateView.as_view(),
        name="book_create_as_admin",
    ),
]
