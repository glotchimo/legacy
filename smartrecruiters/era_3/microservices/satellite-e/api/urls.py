"""
api.urls
~~~~~~~~

This module implements API-level URL configurations for the app.
"""

from api import views

from django.urls import path

urlpatterns = [
    path("accounts", views.get_accounts, name="get-accounts"),
    path("accounts/create", views.create_account, name="create-account"),
    path("accounts/<str:id>/update", views.update_account, name="update-account"),
    path("accounts/<str:id>/delete", views.delete_account, name="delete-account"),
    path("contacts", views.get_contacts, name="get-contacts"),
    path("contacts/create", views.create_contact, name="create-contact"),
    path("contacts/<str:id>/update", views.update_contact, name="update-contact"),
    path("contacts/<str:id>/delete", views.delete_contact, name="delete-contact"),
]
