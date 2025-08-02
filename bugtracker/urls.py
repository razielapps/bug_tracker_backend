# bugtracker/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi






urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.auth_urls')),
    path('api/', include('core.urls')),

        # now you have /api/auth/login, /register, /refresh
]




schema_view = get_schema_view(
   openapi.Info(
      title="Bug Tracker API",
      default_version='v1',
      description="API documentation for the Bug Tracker project",
      terms_of_service="https://www.yoursite.com/terms/",
      contact=openapi.Contact(email="teksomax@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]