from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Allow write access only for admin users
        return request.user and request.user.is_staff
