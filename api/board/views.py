from django.shortcuts import render

from .models import Board
from .serializers import BoardSerializer

from django.contrib.auth import get_user_model

from rest_framework.permissions import (

    SAFE_METHODS,
    BasePermission,
    IsAuthenticated

)
from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_cookie


User = get_user_model()

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return request.user and request.user.is_authenticated

        return request.user and (request.user.is_staff or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return request.user and (obj.customer == request.user or request.user.is_staff or request.user.is_superuser)
        
        return request.user and (request.user.is_staff or request.user.is_superuser)

class BoardViewSet(ModelViewSet):

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BoardSerializer

    def get_queryset(self):

        user = self.request.user

        if user.is_staff or user.is_superuser:
            
            return Board.objects.all()

        return Board.objects.filter(customer=user)
    
         # Aplicar cache nas actions específicas
    @method_decorator(cache_control(max_age=900, private=True))
    @method_decorator(vary_on_cookie)  # Importante para cache por usuário
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_control(max_age=900, private=True))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)