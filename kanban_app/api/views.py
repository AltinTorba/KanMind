# 1. Django
from django.db.models import Count, Q

# 2. Third-party (DRF)
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# 3. Local imports
from kanban_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer


class BoardViewSet(ModelViewSet):
    """Handles CRUD operations for boards."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns boards the user owns or is a member of, with statistics."""
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).annotate(
            member_count=Count("members"),
            ticket_count=Count("tasks"),
            tasks_to_do_count=Count("tasks", filter=Q(tasks__status="to-do")),
            tasks_high_prio_count=Count("tasks", filter=Q(tasks__priority="high"))
        ).distinct()

    def get_serializer_class(self):
        """Returns the appropriate serializer based on the action."""
        if self.action == "list":
            return BoardSerializer
        elif self.action == "retrieve":
            return BoardDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return BoardUpdateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        """Creates a board and assigns the requesting user as owner."""
        board = serializer.save(owner=self.request.user)
        members_data = self.request.data.get('members', [])
        if members_data:
            board.members.set(members_data)

    def partial_update(self, request, *args, **kwargs):
        """Updates board title and/or members. Returns updated board data."""
        board = self.get_object()

        title = request.data.get("title")
        members_data = request.data.get("members")

        if title:
            board.title = title
            board.save()

        if members_data is not None:
            board.members.set(members_data)

        serializer = BoardUpdateSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Deletes a board. Only the owner is allowed to delete."""
        board = self.get_object()

        if board.owner != request.user:
            raise PermissionDenied("You are not the owner of this board.")

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)