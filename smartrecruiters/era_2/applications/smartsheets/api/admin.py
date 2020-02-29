"""
api.admin
~~~~~~~~~

This module implements admin model registrations.
"""

from api.models import Project

from django.contrib import admin


admin.site.register(Project)

