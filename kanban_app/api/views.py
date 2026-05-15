from rest_framework.viewsets import ModelViewSet
from kanban_app.models import Board
from .serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]