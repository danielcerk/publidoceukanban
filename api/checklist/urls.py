from django.urls import path, include
from rest_framework_nested import routers

from api.card.views import CardViewset

from .views import ChecklistViewSet

router = routers.SimpleRouter()
router.register(r'card', CardViewset, basename='card-checklist')

checklists_router = routers.NestedSimpleRouter(router, r'card', lookup='card')
checklists_router.register(r'checklist', ChecklistViewSet, basename='card-checklists')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(checklists_router.urls)),
]
