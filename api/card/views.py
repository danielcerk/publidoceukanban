from django.shortcuts import get_object_or_404

from api.board.models import Board

from .models import Card
from .serializers import (

    CardSerializer,

)

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    IsAuthenticated

)

from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class CardViewset(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):

        board_id = self.kwargs.get('board_pk')

        if board_id is None:

            return Card.objects.none()

        qs = Card.objects.filter(board=board_id).order_by('-created_at')

        if self.request.user.is_superuser or self.request.user.is_staff:

            return qs
        
        return qs.filter(board__customer=self.request.user)

    def perform_create(self, serializer):

        board_id = self.kwargs.get('board_pk')
        board = get_object_or_404(Board, pk=board_id)

        serializer.save(board=board)
        

class DeleteCard1MonthApprovedView(APIView):

    def get(self, request):

        today = timezone.localdate()

        cards_to_delete = Card.objects.filter(deleted_at=today)

        count = 0
        
        for card in cards_to_delete:

            serializer = CardSerializer()
            serializer.delete(card)

            count += 1

        return Response(

            {"message": f"{count} card(s) excluído(s)."},
            status=status.HTTP_200_OK
            
        )