from django.contrib.auth.models import User

from rest_framework import serializers

from tasks_app.models import Task, Comment


class UserMiniSerializer(serializers.ModelSerializer):
    """Serializer for returning minimal user information."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        """Returns the user's full name, username, or email as fallback."""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.get_full_name() or obj.username or obj.email


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for creating, updating, and retrieving tasks."""

    assignee_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    reviewer_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    comments_count = serializers.SerializerMethodField()

    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "reviewer_id",
            "assignee_id",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        """Returns the total number of comments for the task."""
        return obj.comments.count() if hasattr(obj, "comments") else 0

    def create(self, validated_data):
        """Creates a task and assigns assignee and reviewer if provided."""
        assignee_id = validated_data.pop("assignee_id", None)
        reviewer_id = validated_data.pop("reviewer_id", None)

        task = Task.objects.create(**validated_data)

        if assignee_id:
            task.assignee_id = assignee_id
        if reviewer_id:
            task.reviewer_id = reviewer_id

        task.save()
        return task

    def update(self, instance, validated_data):
        """Updates a task including assignee and reviewer if provided."""
        assignee_id = validated_data.pop("assignee_id", None)
        reviewer_id = validated_data.pop("reviewer_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if assignee_id is not None:
            instance.assignee_id = assignee_id

        if reviewer_id is not None:
            instance.reviewer_id = reviewer_id

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving comments."""

    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "created_at",
            "author",
            "content",
        ]

    def get_author(self, obj):
        """Returns the author's full name, username, or email as fallback."""
        author = obj.author
        return author.get_full_name() or author.username or author.email


