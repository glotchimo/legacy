"""
satellite_s.urls
~~~~~~~~~~~~~~~~

This module implements high-level URL configurations.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("", include("api.urls"))]
