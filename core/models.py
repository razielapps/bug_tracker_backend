from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DEVELOPER = 'developer', 'Developer'
        REPORTER = 'reporter', 'Reporter'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REPORTER
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open'
        IN_PROGRESS = 'in_progress'
        CLOSED = 'closed'

    class Priority(models.TextChoices):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.project.name}"


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.issue.title}"


class AuditLog(models.Model):
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('assign', 'Assign'),
        ('comment', 'Comment'),
    ]

    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.actor} {self.action} at {self.timestamp}"

