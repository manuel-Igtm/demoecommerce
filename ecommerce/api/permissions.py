from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access to admins, but read-only for everyone else.
    Good for Product/Category management.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Allow users to only access their own objects,
    unless they are admins.
    Useful for Orders & Carts.
    """
    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user and request.user.is_staff:
            return True

        # Check ownership (works for Order, Cart, etc.)
        if hasattr(obj, "created_by"):
            return obj.created_by == request.user
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False


class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    Allow unauthenticated users to create (e.g. sign up),
    but require authentication for everything else.
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated

