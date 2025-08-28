from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from drf_spectacular.views import SpectacularRedocView

urlpatterns = [

    path('api/v1/', include('api.urls')),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]

if settings.DEBUG:

    urlpatterns.append(path("admin/", admin.site.urls))