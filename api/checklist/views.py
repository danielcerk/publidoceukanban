from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from .models import Checklist
from .serializers import ChecklistSerializer

from rest_framework.permissions import (

    IsAdminUser

)

from api.card.models import Card

class ChecklistViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ChecklistSerializer

    def get_queryset(self):

        card_id = self.kwargs.get('card_pk')
        user = self.request.user

        if card_id is None:

            return Checklist.objects.none()

        if user.is_staff or user.is_superuser:

            return Checklist.objects.filter(card_id=card_id).order_by('-id')

        return Checklist.objects.none()

    def perform_create(self, serializer):
        
        card_id = self.kwargs.get('card_pk')
        card = get_object_or_404(card, pk=card_id)

        serializer.save(card=card)
