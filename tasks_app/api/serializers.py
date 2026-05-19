from rest_framework import serializers
from django.contrib.auth.models import User
from tasks_app.models import Task


# 👤 Mini user serializer (për assignee/reviewer)
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# 🧠 MAIN TASK SERIALIZER
class TaskSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

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
            "comments_count",
        ]

    # 📊 custom field: number of comments
    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, "comments") else 0