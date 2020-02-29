"""
api.urls
~~~~~~~~

This module implements API-level URL configurations for the app.
"""

from api import views

from django.urls import path

urlpatterns = [
    path("<str:model_name>", views.get, name="get"),
    path("<str:model_name>/create", views.create, name="create"),
    path("<str:model_name>/<str:id>/update", views.update, name="update"),
    path("<str:model_name>/<str:id>/delete", views.delete, name="delete"),
]
