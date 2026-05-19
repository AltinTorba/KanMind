from django.contrib.auth.models import User
from rest_framework import serializers
from kanban_app.models import Board
from tasks_app.models import Task

        
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        
        
class TaskMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status"]

class TaskDetailMiniSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer()
    reviewer = UserMiniSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "priority",
            "assignee",
            "reviewer"
        ]
        
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title", "owner", "members"]

        extra_kwargs = {
            "owner": {"read_only": True},
            "members": {"required": False}
        }
        
        
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserMiniSerializer(many=True, read_only=True)
    tasks = TaskDetailMiniSerializer(many=True, read_only=True)


    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner",
            "members",
            "tasks",
        ]