"""
app.urls
~~~~~~~~

This module implements app-level URL configuration for Pathfindr.
"""

from app import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<str:sfid>/', views.enrich, name='enrich')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

