from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and request.user == obj.user)
    