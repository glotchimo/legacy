"""
api.models
~~~~~~~~~~

This module implements the database models for the API.
"""

import os
import uuid

from django.db import models

import requests
from bs4 import BeautifulSoup
from simple_history.models import HistoricalRecords


class Competitor(models.Model):
    """ Models a given competitor. """

    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)

    name = models.CharField("Name", max_length=128)
    website = models.URLField("Website")
    description = models.TextField("Description", max_length=32000)

    strengths = models.TextField(
        "Key Strengths", max_length=2048, default="No key strengths added."
    )
    pricing = models.TextField(
        "Pricing Details", max_length=2048, default="No pricing information available."
    )
    wins = models.TextField(
        "Replacement Wins", max_length=2048, default="No replacement wins recorded."
    )

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return str(self.name)


class Advantage(models.Model):
    """ Models a SmartAdvantage. """

    datestamp = models.DateField("Datestamp", auto_now_add=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    competitor = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="advantages",
        related_query_name="advantage",
    )

    name = models.CharField("Name", max_length=256)
    script = models.TextField("Script", max_length=2048)

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return f"{self.competitor} - {self.name}"


class Objection(models.Model):
    """ Models an objection/handler. """

    datestamp = models.DateField("Datestamp", auto_now_add=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    competitor = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="objections",
        related_query_name="objection",
    )

    name = models.CharField("Name", max_length=256)
    script = models.TextField("Script", max_length=2048)

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return f"{self.competitor} - {self.name}"


class Resource(models.Model):
    """ Modelse a standalone resource. """

    timestamp = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    competitor = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="resources",
        related_query_name="resource",
    )

    title = models.CharField("Title", max_length=256, default="New Resource")
    link = models.URLField("Link", null=True, blank=True)
    description = models.TextField("Description", max_length=32000, default="")
    status = models.CharField("Status", max_length=64, default="approved")

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return f"{self.competitor} - {self.title}"


class Insight(models.Model):
    """ Models a insight about a competitor. """

    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    competitor = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="insights",
        related_query_name="insight",
    )

    title = models.CharField("Title", max_length=64, default="New Insight")
    link = models.URLField("Link", null=True, blank=True)
    description = models.TextField("Description", max_length=32000, default="")
    status = models.CharField("Status", max_length=64, default="approved")

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """ Models a comment on a dissussion. """

    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    insight = models.ForeignKey(
        Insight,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )

    content = models.TextField("Content", max_length=2048)

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return str(self.insight)


class Page(models.Model):
    datestamp = models.DateField("Datestamp", auto_now_add=True)
    history = HistoricalRecords()

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    competitor = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="pages",
        related_query_name="page",
    )

    url = models.URLField("Page URL")
    content = models.TextField("Page Content", max_length=32000, null=True, blank=True)

    def __id__(self):
        return str(self.id)

    def __str__(self):
        return f"{self.competitor} - {self.url} - {self.datestamp}"

    def update(self):
        r = requests.get(self.url)

        soup = BeautifulSoup(r.content, features="html.parser")
        content = soup.get_text().strip()

        self.content = content
        self.save()
