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
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()
        
        
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