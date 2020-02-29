"""
smartsheets.urls
~~~~~~~~~~

This module implements the high-level URL configurations.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import urls as auth_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(auth_urls)),
    path('', include('app.urls', namespace='app')),
    path('api', include('api.urls', namespace='api'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)