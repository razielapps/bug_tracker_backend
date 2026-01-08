from rest_framework import serializers
from .models import Project, Issue, Comment, AuditLog
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
            'password2',
            'role',
            'bio',
            'first_name'
        )
        extra_kwargs = {
            'role': {'required': False},
            'email': {'required': True},
            'first_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

# serializers.py

class ProjectMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")

    class Meta:
        model = CustomUser
        fields = ["id", "name", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    members = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False
    )

    members_detail = ProjectMemberSerializer(
        source="members",
        many=True,
        read_only=True
    )

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]




class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "issue", "text", "user_name", "created_at"]
        read_only_fields = ["user_name", "created_at"]

    def validate_issue(self, issue):
        request = self.context.get("request")
        user = request.user

        # Admin can comment anywhere
        if user.role == "admin":
            return issue

        # Only issue creator or assignee can comment
        if issue.created_by != user and issue.assigned_to != user:
            raise serializers.ValidationError(
                "You are not allowed to comment on this issue."
            )

        return issue

class IssueSerializer(serializers.ModelSerializer):
    # ✅ WRITE: accept project ID
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only=True
    )

    # ✅ READ: human-friendly fields
    project_name = serializers.CharField(source="project.name", read_only=True)
    assigned_to = serializers.CharField(source="assigned_to.username", read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class AuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    issue_title = serializers.CharField(source='issue.title', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'action', 'actor', 'actor_username', 'issue', 'issue_title', 'project', 'project_name', 'timestamp']
        read_only_fields = ['actor', 'actor_username', 'timestamp']
