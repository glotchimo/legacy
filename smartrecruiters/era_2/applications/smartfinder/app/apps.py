"""
app.apps
~~~~~~~~

This module implements the Django app configuration.
"""

from django.apps import AppConfig as Config


class AppConfig(Config):
    name = 'app'
