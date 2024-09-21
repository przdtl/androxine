from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if not request.user.is_staff:
            return request.method in SAFE_METHODS

        return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            return request.user.is_staff

        return False
