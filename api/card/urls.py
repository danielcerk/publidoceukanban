from django.urls import path, include
from rest_framework_nested import routers

from api.board.views import BoardViewSet

from .views import CardViewset

router = routers.SimpleRouter()
router.register(r'board', BoardViewSet, basename='board-card')

cards_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
cards_router.register(r'card', CardViewset, basename='board-cards')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cards_router.urls)),
]
