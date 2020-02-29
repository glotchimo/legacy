"""
satellite_e.urls
~~~~~~~~~~~~~~~~

This mopdule implements high-level URL configurations.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("", include("api.urls"))]
