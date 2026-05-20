from rest_framework.viewsets import ModelViewSet
from tasks_app.models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            board__members=self.request.user
        ).distinct()
        
    def perform_create(self, serializer):
        board = serializer.validated_data["board"]

        if self.request.user not in board.members.all():
            raise PermissionDenied("Not allowed")

        serializer.save()
        
    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        tasks = Task.objects.filter(
            assignee=request.user
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="reviewing")
    def reviewing(self, request):
        tasks = Task.objects.filter(
            reviewer=request.user
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)