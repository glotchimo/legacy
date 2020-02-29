"""
app.urls
~~~~~~~~

This module implements the app-level URL configurations.

:copyright: (c) 2019 by Elliott Maguire
"""

from app import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/<str:sfid>', views.account, name='account'),
    path('accounts/<str:sfid>/edit', views.edit, name='edit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
