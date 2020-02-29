"""
ax-s.urls
~~~~~~~~~

This module implements high-level URL configurations for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='app')),
    path('api/', include('api.urls', namespace='api')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
