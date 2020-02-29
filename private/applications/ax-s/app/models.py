"""
app.models
~~~~~~~~~

This module implements the web database models for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

from api.models import API, Endpoint

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """ User profile model. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField('Access Token', max_length=256)

