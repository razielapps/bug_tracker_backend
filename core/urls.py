from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet, CommentViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'auditlogs', AuditLogViewSet)

urlpatterns = router.urls
