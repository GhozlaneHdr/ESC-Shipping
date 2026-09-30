"""
Custom permissions for user management.
"""

from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Allow access if the user is an admin or the object owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj == request.user


class IsAdmin(permissions.BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"
