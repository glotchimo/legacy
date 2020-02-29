"""
pathfindr.urls
~~~~~~~~~~~~~~

This module implements high-level URL configuration for Pathfindr.
"""

from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(auth_urls)),
    path('', include("app.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

