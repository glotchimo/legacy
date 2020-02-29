"""
api.models
~~~~~~~~~~

This module implements the API models.

:copyright: (c) 2019 by Elliott Maguire
"""

from django.db import models


class Account(models.Model):
    date_added = models.DateField('Date Added', auto_now=True)

    sfid = models.CharField('Salesforce ID', max_length=32)
    doid = models.CharField('DiscoverOrg ID', max_length=256, null=True, blank=True)
    prep = models.CharField('Prospecting Rep', max_length=64, null=True, blank=True)
    status = models.CharField('Status', max_length=16, default='enrich')

    name = models.CharField('Name', max_length=64)
    domain = models.URLField('Domain')
    phone = models.CharField('Office Phone', max_length=64, null=True, blank=True)

    hierarchy = models.TextField('Org Hierarchy', max_length=65536, null=True, blank=True)
    insight = models.TextField('Insight', max_length=2048, null=True, blank=True)
    summary = models.TextField('Enrichment Summary', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    sfid = models.CharField('Salesforce ID', max_length=32, blank=True, null=True)
    doid = models.CharField('DiscoverOrg ID', max_length=256, blank=True, null=True)
    ctype = models.CharField('Type', max_length=16, default='new')
    status = models.CharField('Status', max_length=16, default='enrich')
    patched = models.BooleanField('Patched', default=False)

    rating = models.CharField('Rating', max_length=8, blank=True, null=True, default=4)
    priority = models.CharField('Priority', max_length=8, blank=True, null=True, default=6)

    name = models.CharField('Name', max_length=128)
    title = models.CharField('Title', max_length=128, null=True, blank=True, default='')

    email = models.EmailField('Email', null=True, blank=True)
    office = models.CharField('Office Line', max_length=32, null=True, blank=True, default='')
    direct = models.CharField('Direct Line', max_length=32, null=True, blank=True, default='')
    mobile = models.CharField('Mobile Phone', max_length=32, null=True, blank=True, default='')

    def __str__(self):
        return self.name

