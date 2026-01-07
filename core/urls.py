from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
    AuditLogViewSet,
    RegisterView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"auditlogs", AuditLogViewSet, basename="auditlog")

urlpatterns = [
    path("", include(router.urls)),  # all your viewsets
    path(
        "auth/register/", RegisterView.as_view(), name="auth_register"
    ),  # RegisterView
    path(
        "auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT login
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT refresh
]
