"""
api.admin
~~~~~~~~~

This module implements the API admin model registration for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

from api.models import API, Endpoint, Error

from django.contrib import admin


admin.site.register(API)
admin.site.register(Endpoint)
admin.site.register(Error)

