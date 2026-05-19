from rest_framework.viewsets import ModelViewSet
from kanban_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer
from rest_framework.permissions import IsAuthenticated


class BoardViewSet(ModelViewSet):
    # queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Board.objects.filter(
            members=self.request.user
        ).distinct()
        
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        return BoardSerializer