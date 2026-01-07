# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project, Comment, Issue


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role", "bio", "avatar")}),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "issue",
        "user",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("issue__title", "user__username", "content")
    ordering = ("-created_at",)


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "project",
        "status",
        "priority",
        "assigned_to",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at", "project")
    search_fields = (
        "title",
        "description",
        "created_by__username",
        "assigned_to__username",
    )
    ordering = ("-created_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_by",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("name", "description", "created_by__username")
    ordering = ("-created_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_header = "Bug Tracker Admin"
admin.site.site_title = "Bug Tracker Admin Portal"
admin.site.index_title = "Welcome to the Bug Tracker Admin Portal"
# admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
