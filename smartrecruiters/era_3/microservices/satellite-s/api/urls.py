"""
api.urls
~~~~~~~~

This module implements API-level URL configurations for the app.
"""

from django.urls import path
from api import views

urlpatterns = [
    path("create", views.create_user, name="create-user"),
    path("confirm", views.confirm_user, name="confirm-user"),
    path("get", views.get_users, name="get-user"),
    path("authenticate", views.authenticate, name="authenticate"),
    path("authorize", views.authorize, name="authorize"),
]
