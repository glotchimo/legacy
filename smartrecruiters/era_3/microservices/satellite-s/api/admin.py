"""
api.admin
~~~~~~~~~

This module implements the admin terminal configuration for the API.
"""

from api.models import Profile

from django.contrib import admin


admin.site.register(Profile)
