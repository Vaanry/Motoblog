"""Permissions."""

from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """AuthorOrReadOnly."""

    def has_permission(self, request, view):
        """has_permission."""
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        """has_object_permission."""
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """ReadOnly."""

    def has_permission(self, request, view):
        """has_permission."""
        return request.method in permissions.SAFE_METHODS
