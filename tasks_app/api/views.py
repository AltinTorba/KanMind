from rest_framework.viewsets import ModelViewSet
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()
        
    def perform_create(self, serializer):
        board = serializer.validated_data["board"]
        user = self.request.user
        
        if board.owner != user and user not in board.members.all():
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
    
    
class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        comments = task.comments.all()

        serializer = CommentSerializer(
            comments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        serializer = CommentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                task=task,
                author=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, task_id, comment_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        comment = get_object_or_404(
            Comment,
            id=comment_id,
            task=task
        )

        if comment.author != request.user and task.board.owner != request.user:
            raise PermissionDenied("Not allowed")

        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)