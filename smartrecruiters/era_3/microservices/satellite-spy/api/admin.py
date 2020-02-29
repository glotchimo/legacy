"""
api.admin
~~~~~~~~~

This module implements the admin terminal configuration for the API.
"""

from api.models import (
    Competitor,
    Advantage,
    Objection,
    Resource,
    Insight,
    Comment,
    Page,
)

from django.contrib import admin

admin.site.register(Competitor)
admin.site.register(Advantage)
admin.site.register(Objection)
admin.site.register(Resource)
admin.site.register(Insight)
admin.site.register(Comment)
admin.site.register(Page)
