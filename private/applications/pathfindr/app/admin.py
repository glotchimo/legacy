"""
app.admin
~~~~~~~~~

This module implements the admin model registry for Pathfindr.
"""

from app.models import Account, Contact

from django.contrib import admin


admin.site.register(Account)
admin.site.register(Contact)