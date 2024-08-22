from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if not request.user.is_staff:
            return request.method in SAFE_METHODS

        return True
