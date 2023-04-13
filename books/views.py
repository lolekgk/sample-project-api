from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Book
from .pagination import DefaultPagination
from .permissions import IsBookOwner
from .serializers import BookListCreateSerializer, BookUpdateSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListCreateSerializer
    pagination_class = DefaultPagination


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
    permission_classes = [IsBookOwner]
