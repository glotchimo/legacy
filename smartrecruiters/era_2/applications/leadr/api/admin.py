"""
api.admin
~~~~~~~~~

This module implements the admin model registrations.

:copyright: (c) 2019 by Elliott Maguire
"""

from api.models import Account, Contact

from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    search_fields = ['name', 'sfid', 'doid', 'status']


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['name', 'sfid', 'doid', 'status']


admin.site.register(Account, AccountAdmin)
admin.site.register(Contact, ContactAdmin)

