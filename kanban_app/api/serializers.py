from rest_framework import serializers
from kanban_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        
        extra_kwargs = {
            "owner": {"read_only": True},
            "members": {"required": False}
        }