"""
api.models
~~~~~~~~~~

This module implements the database models for the API.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cid = models.CharField("Confirmation ID", max_length=36)
    status = models.CharField("User Status", max_length=9, default="pending")

    sfid = models.CharField("Salesforce ID", max_length=18)
    token = models.CharField("Access Token", max_length=43)

    alignment = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="aligments",
        related_query_name="alignment",
    )

    spy_subs = models.CharField(
        "SmartSpy Subscriptions", max_length=32000, null=True, blank=True, default=""
    )

    def __str__(self):
        return str(self.user)
