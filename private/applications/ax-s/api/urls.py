"""
api.urls
~~~~~~~~

This module implements the API URL configurations for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

app_name = 'api'

urlpatterns = [
    path('call/<str:token>', views.caller, name='call'),
    path('apis/add', views.api_add, name='api-add'),
    path('apis/<str:name>/delete', views.api_delete, name='api-delete'),
    path('endpoints/<str:name>/add', views.endpoint_add, name='endpoint-add'),
    path('endpoints/<str:name>/<str:endpoint>/edit', views.endpoint_edit, name='endpoint-edit'),
    path('endpoints/<str:name>/<str:endpoint>/delete', views.endpoint_delete, name='endpoint-delete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

