from django.contrib.auth.models import User

from rest_framework import serializers

from kanban_app.models import Board
from tasks_app.models import Task


class UserMiniSerializer(serializers.ModelSerializer):
    """Serializer for returning minimal user information."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        """Returns the user's full name or username as fallback."""
        return obj.get_full_name() or obj.username


class TaskMiniSerializer(serializers.ModelSerializer):
    """Serializer for returning minimal task information."""

    class Meta:
        model = Task
        fields = ["id", "title", "status"]


class TaskDetailMiniSerializer(serializers.ModelSerializer):
    """Serializer for returning detailed task information inside a board."""

    assignee = UserMiniSerializer()
    reviewer = UserMiniSerializer()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        """Returns the total number of comments for the task."""
        return obj.comments.count()


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for returning board list with statistics."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def get_member_count(self, obj):
        """Returns the total number of board members."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks in the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with status 'to-do'."""
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks with high priority."""
        return obj.tasks.filter(priority="high").count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer for returning full board details including members and tasks."""

    members = UserMiniSerializer(many=True, read_only=True)
    tasks = TaskDetailMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating board title and members."""

    owner_data = UserMiniSerializer(source="owner", read_only=True)
    members_data = UserMiniSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_data",
            "members_data",
        ]


