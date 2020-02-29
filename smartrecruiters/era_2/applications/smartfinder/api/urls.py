"""
api.urls
~~~~~~~~

This module implements the API-level URL configurations.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


app_name = 'api'

urlpatterns = [
    path('edit-account/<str:sfid>', views.edit_account, name='edit-account'),
    path('mark-account/<str:sfid>/<str:status>', views.mark_account, name='mark-account'),
    path('get-hierarchy/<str:sfid>', views.get_hierarchy, name='get-hierarchy'),
    path('cancel-enrichment/<str:sfid>', views.cancel_enrichment, name='cancel-enrichment'),
    path('add-contact/<str:sfid>', views.add_contact, name='add-contact'),
    path('mark-contact/<str:cid>/<str:status>', views.mark_contact, name='mark-contact'),
    path('edit-contact/<str:cid>', views.edit_contact, name='edit-contact'),
    path('queue-contact/<str:cid>', views.queue_contact, name='queue-contact'),
    path('queue-contacts/<str:sfid>', views.queue_contacts, name='queue-contacts'),
    path('delete-contact/<str:cid>', views.delete_contact, name='delete-contact')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
