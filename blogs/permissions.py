from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):
    # User must be authenticated.
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    # Only the owner can view their subscribed to posts.
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of a post
        return obj.author == request.user

    # Need to study how permissions source code works in django rest framework.
