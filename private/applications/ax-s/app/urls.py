"""
app.urls
~~~~~~~~~

This module implements the web URL configurations for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

from app import views

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import urls as auth_urls


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('docs', views.docs, name='docs'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('apis', views.apis, name='apis'),
    path('apis/<str:name>', views.view, name='view'),
    path('apis/<str:name>/edit', views.edit, name='edit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

