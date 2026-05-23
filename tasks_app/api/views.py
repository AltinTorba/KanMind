from rest_framework.viewsets import ModelViewSet
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.http import Http404


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
    
    def get_object(self):
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
        board = serializer.validated_data.get("board")
        user = self.request.user
        
        if not board:
            raise PermissionDenied("Board is required")
        
        if board.owner != user and user not in board.members.all():
            raise PermissionDenied("Not allowed")
        
        serializer.save(created_by=user)

    
    def perform_update(self, serializer):
        task = self.get_object()
        
        if 'board' in self.request.data:
            raise PermissionDenied("Changing board is not allowed")
        
        # if task.status == 'completed':
        #     raise PermissionDenied("Cannot update completed task")
        
        serializer.save()
        
    def destroy(self, request, *args, **kwargs):
        task = self.get_object() 
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="reviewing")
    def reviewing(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    
class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")
        
        comments = task.comments.all().order_by('created_at')
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")
        
        serializer = CommentSerializer(data=request.data)
        
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
        
        if task.board.owner != request.user and request.user not in task.board.members.all():
            raise PermissionDenied("Not allowed")
        
        comment = get_object_or_404(Comment, id=comment_id, task=task)
        
        if comment.author != request.user:
            raise PermissionDenied("Not allowed")
        
        comment.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)