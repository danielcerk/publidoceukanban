from django.urls import path

from .views import NotificationListView

urlpatterns = [

    path('notification/', NotificationListView.as_view(), name='notification')

]