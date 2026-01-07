from django.db.models import Q
from rest_framework import generics, viewsets, permissions, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import CustomUser, Project, Issue, Comment, AuditLog
from .serializers import (
    RegisterSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    AuditLogSerializer,
)
from .permissions import (
    IsProjectCreatorOrReadOnly,
    IsIssueEditor,
)


# =========================
# AUTH
# =========================

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# =========================
# PROJECTS
# =========================

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =========================
# ISSUES
# =========================

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueEditor]

    def get_queryset(self):
        user = self.request.user
        qs = Issue.objects.all()

        # 🔐 Non-admin visibility
        if user.role != "admin":
            qs = qs.filter(
                Q(created_by=user) |
                Q(assigned_to=user)
            )

        # Optional project scoping (URL-based)
        project_id = self.kwargs.get("project_id")
        if project_id:
            qs = qs.filter(project_id=project_id)

        return qs

    def perform_create(self, serializer):
        # ✅ Project MUST come from request body
        project = serializer.validated_data.get("project")

        if not project:
            raise serializers.ValidationError(
                {"project": "Project is required."}
            )

        # 🔐 Only project members can create issues
        if self.request.user not in project.members.all():
            raise PermissionDenied(
                "You are not a member of this project."
            )

        serializer.save(created_by=self.request.user)


# =========================
# COMMENTS 
# =========================

# views.py

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("issue", "user")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Comment.objects.all()
        issue_id = self.request.query_params.get("issue")

        if issue_id:
            qs = qs.filter(issue_id=issue_id)

        return qs.order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# =========================
# AUDIT LOGS
# =========================

class IsAuditViewer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Project owner
        if obj.project:
            return obj.project.created_by == request.user

        # Issue participants
        if obj.issue:
            return (
                obj.issue.created_by == request.user or
                obj.issue.assigned_to == request.user
            )

        return False


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by("-timestamp")
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuditViewer]

    def get_queryset(self):
        user = self.request.user
        return AuditLog.objects.filter(
            Q(project__created_by=user) |
            Q(issue__created_by=user) |
            Q(issue__assigned_to=user)
        )
