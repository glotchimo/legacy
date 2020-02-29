"""
satellite_spy.urls
~~~~~~~~~~~~~~~~

This mopdule implements high-level URL configurations.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("api/", include("api.urls"))]
