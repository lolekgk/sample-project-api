from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Book


class IsBookOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: Book
    ) -> bool:
        return obj.owner == request.user
