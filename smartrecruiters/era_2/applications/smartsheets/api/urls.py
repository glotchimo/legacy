"""
api.urls
~~~~~~~~

This module implements API-level URL configurations.
"""

from api import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


app_name = 'api'

urlpatterns = [
    path('projects/create', views.create_project, name='create-project'),
    path('projects/mark/<str:pid>/<str:status>', views.mark_project, name='mark-project'),
    path('projects/delete/<str:pid>', views.delete_project, name='delete-project'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)