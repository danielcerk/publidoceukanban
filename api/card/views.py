from django.shortcuts import get_object_or_404

from api.board.models import Board

from .models import Card
from .serializers import (

    CardSerializer,

)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    IsAuthenticated

)

class CardViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        board_id = self.kwargs.get('board_pk')
        if board_id is None:
            return Card.objects.none()  # evita erros se acessado sem board_pk

        qs = Card.objects.filter(board=board_id).order_by('-created_at')
        if self.request.user.is_superuser or self.request.user.is_staff:
            return qs
        return qs.filter(board__customer=self.request.user)

    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_pk')
        board = get_object_or_404(Board, pk=board_id)

        serializer.save(board=board)
