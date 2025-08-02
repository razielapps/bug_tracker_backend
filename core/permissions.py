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
