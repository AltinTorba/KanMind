from rest_framework.viewsets import ModelViewSet
from tasks_app.models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

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
            raise PermissionError("Not allowed")

        serializer.save()