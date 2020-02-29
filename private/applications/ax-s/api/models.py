"""
api.views
~~~~~~~~~

This module implements the API database models for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

import uuid

from django.db import models
from django.contrib.auth.models import User


class Error(models.Model):
    """ Error reporting model. """
    time = models.TimeField('Time', auto_now=True)

    api = models.ForeignKey('API', on_delete=models.CASCADE)
    endpoint = models.ForeignKey('Endpoint', on_delete=models.CASCADE)

    traceback = models.TextField('Captured Traceback', max_length=8192)

    def __str__(self):
        return str(self.time)


class APIManager(models.Manager):
    def create_api(self, user):
        token = uuid.uuid4().hex
        id = token[::2][::2]
        api = self.create(
            id=id,
            user=user,
            token=token,
            name=id,
            base='',
            auth=1)

        return api

class API(models.Model):
    """ Base API model.  """
    objects = APIManager()

    id = models.CharField('ID', max_length=16, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField('Access Token', max_length=256)

    name = models.CharField('Name', max_length=64)
    base = models.URLField('Base URL')
    description = models.TextField('Description', max_length=256)

    METHODS = ((1, 'none'), (2, 'basic'), (3, 'header'), (4, 'params'))
    auth = models.PositiveSmallIntegerField('Auth Method', choices=METHODS, default=METHODS[0])

    username = models.CharField('Username', max_length=256, blank=True, null=True)
    password = models.CharField('Password', max_length=512, blank=True, null=True)

    key = models.CharField('Key', max_length=512, blank=True, null=True)
    keyname = models.CharField('Key Name', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Endpoint(models.Model):
    """ API endpoint model. """
    api = models.ForeignKey(API, on_delete=models.CASCADE)

    name = models.CharField('Name', max_length=64)
    path = models.CharField('Path from Base', max_length=256)
    description = models.TextField('Description', max_length=256, blank=True, null=True)

    METHODS = ((1, 'GET'), (2, 'POST'), (3, 'PUT'), (4, 'PATCH'), (5, 'DELETE'))
    method = models.PositiveSmallIntegerField('HTTP Method', choices=METHODS, default=METHODS[1])

    headers = models.CharField('Request Headers', max_length=2048, blank=True, null=True, default='{}')
    params = models.CharField('URL Parameters', max_length=2048, blank=True, null=True, default='{}')
    body = models.CharField('Request Body', max_length=2048, blank=True, null=True, default='{}')
    targets = models.CharField('Data Targets', max_length=2048, blank=True, null=True, default=[])

    calls = models.IntegerField('Calls', default=0)

    def __str__(self):
        return self.name

