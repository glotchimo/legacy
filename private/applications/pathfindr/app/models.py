"""
app.models
~~~~~~~~~~

This module implements the database models for Pathfindr.

:copyright: (c) 2018 by Elliott Maguire
"""

from django.db import models


class Account(models.Model):
    """ Abstracts the Account model.

    Built loosely after the Salesforce account object to retain parallelism, 
    only contains necessary information as well as status tracking fields
    for use in Pathfindr.
    
    """
    sfid = models.CharField('Salesforce ID', max_length=32, blank=True)
    name = models.CharField('Company Name', max_length=356, blank=True)
    domain = models.URLField('Company Website', null=True, blank=True)
    phone = models.CharField('Office Phone', max_length=32, null=True, blank=True)

    date_created = models.TimeField('Date Imported', auto_now=True)
    date_updated = models.TimeField('Date Updated', auto_now_add=True)

    status = models.CharField('Status', max_length=32, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """ Abstracts the Contact model.

    Includes fields for all datasources, as well as
    status tracking fields for use in Pathfindr.
    
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    sfid = models.CharField('Salesforce ID', max_length=256, null=True, blank=True)
    dorgid = models.CharField('DiscoverOrg ID', max_length=64, null=True, blank=True)
    name = models.CharField('Name', max_length=256)
    title = models.CharField('Title', max_length=256, null=True, blank=True)

    email = models.EmailField('Email', null=True, blank=True)
    direct = models.CharField('Direct Line', max_length=32, null=True, blank=True)
    mobile = models.CharField('Mobile Phone', max_length=32, null=True, blank=True)

    rating = models.CharField('Rating', max_length=8, null=True, blank=True)
    status = models.CharField('Status', max_length=32, blank=True)

    def __str__(self):
        return self.name

