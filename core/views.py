from rest_framework import generics,viewsets, permissions, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Project, Issue, Comment, AuditLog
from .serializers import RegisterSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, AuditLogSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import viewsets, permissions
from .permissions import IsProjectCreatorOrReadOnly, IsIssueAssigneeOrReadOnly



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueAssigneeOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'status', 'created_at']

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.query_params.get('project')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        assignee = self.request.query_params.get('assigned_to')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if assignee:
            queryset = queryset.filter(assigned_to__id=assignee)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class IsProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only members of the same project as the issue
        return obj.issue.project.members.filter(id=request.user.id).exists()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class IsAuditViewer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow viewing if user is part of the related project or issue
        if obj.project and request.user in obj.project.members.all():
            return True
        if obj.issue and request.user in obj.issue.project.members.all():
            return True
        return False

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuditViewer]

    def get_queryset(self):
        user = self.request.user
        return AuditLog.objects.filter(
            project__members=user
        ) | AuditLog.objects.filter(
            issue__project__members=user
        )

