# 1. Django
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

# 2. Third-party (DRF)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# 3. Local imports
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer


class TaskViewSet(ModelViewSet):
    """Handles CRUD operations for tasks."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns tasks belonging to boards the user owns or is a member of."""
        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()

    def get_object(self):
        """Returns a task if it exists and the user has permission to access it."""
        try:
            task = Task.objects.get(pk=self.kwargs['pk'])
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

        user = self.request.user
        board = task.board

        if self.action in ['retrieve', 'update', 'partial_update']:
            if board.owner != user and user not in board.members.all():
                raise PermissionDenied(detail="Not allowed")

        if self.action == 'destroy':
            if board.owner != user and task.created_by != user:
                raise PermissionDenied(detail="Not allowed")

        return task

    def perform_create(self, serializer):
        """Creates a task if the user is a board member or owner."""
        board = serializer.validated_data.get("board")
        user = self.request.user

        if not board:
            raise PermissionDenied("Board is required")

        if board.owner != user and user not in board.members.all():
            raise PermissionDenied("Not allowed")

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        """Updates a task. Changing the board is not allowed."""
        if 'board' in self.request.data:
            raise PermissionDenied("Changing board is not allowed")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Deletes a task. Returns 204 on success."""
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        """Returns all tasks assigned to the authenticated user."""
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="reviewing")
    def reviewing(self, request):
        """Returns all tasks where the authenticated user is the reviewer."""
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class CommentListCreateView(APIView):
    """Handles listing, creating, and deleting comments for a task."""

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        """Returns all comments for a task if the user is a board member."""
        task = get_object_or_404(Task, id=task_id)

        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        """Creates a comment for a task if the user is a board member."""
        task = get_object_or_404(Task, id=task_id)

        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(task=task, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, comment_id):
        """Deletes a comment if the user is the author."""
        task = get_object_or_404(Task, id=task_id)

        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")

        comment = get_object_or_404(Comment, id=comment_id, task=task)

        if comment.author != request.user:
            raise PermissionDenied("Not allowed")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)