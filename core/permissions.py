from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsProjectCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.created_by == request.user
        )

class IsIssueAssigneeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.assigned_to == request.user
        )
from rest_framework import permissions

class IsProjectCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.created_by == request.user
        )

class IsIssueAssigneeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.assigned_to == request.user
        )
from rest_framework import permissions

class IsProjectCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.created_by == request.user
        )


class IsStaffProjectCreatorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Only staff users can create projects
        if view.action == "create":
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # Read-only for everyone authenticated
        if request.method in SAFE_METHODS:
            return True

        # Only creator or admin can edit
        return (
            request.user.is_staff and
            (obj.created_by == request.user or request.user.role == "admin")
        )


class IsIssueAssigneeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.assigned_to == request.user
        )



class IsIssueEditor(BasePermission):
    """
    Allow:
    - Read for authenticated users
    - Write for:
        - Issue creator
        - Assigned user
        - Admin
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if user.role == 'admin':
            return True

        if obj.created_by == user:
            return True

        if obj.assigned_to == user:
            return True

        return False


class IsIssueParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        issue = obj.issue

        return (
            user == issue.created_by or
            user == issue.assigned_to or
            user.role == 'admin'
        )


