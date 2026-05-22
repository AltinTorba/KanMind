from django.db.models import Count, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from kanban_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer


class BoardViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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
        if self.action == "list":
            return BoardSerializer
        elif self.action == "retrieve":
            return BoardDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return BoardUpdateSerializer  # ✅ Për PATCH
        return BoardSerializer

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        members_data = self.request.data.get('members', [])
        if members_data:
            board.members.set(members_data)