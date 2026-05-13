from rest_framework.viewsets import ModelViewSet
from kanban_app.models import Board
from .serializers import BoardSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer