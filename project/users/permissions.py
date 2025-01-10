from rest_framework import permissions

class IsAuthenticatedOrReadLimited(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True                           # Authenticated users have full access
        if request.method in permissions.SAFE_METHODS:
            return True                           # Allow read-only access for unauthenticated users
        return False                              # Denied permissions other methods (POST, PUT, DELETE) for unauthenticated users
