"""
app.models
~~~~~~~~~~
This module implements the app models.
:copyright: (c) 2019 by Elliott Maguire
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    sfid = models.CharField(
        'Salesforce ID', max_length=64, null=True, blank=True)

    def __str__(self):
        return str(self.user)

