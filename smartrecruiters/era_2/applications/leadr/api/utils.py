"""
api.utils
~~~~~~~~~

This module implements the utility methods.

:copyright: (c) 2019 by Elliott Maguire
"""

import os

from api.models import Account, Contact
from api.clients import SalesforceClient, DiscoverOrgClient, LushaClient


def enrich_contact(contact):
    """ Enriches a contact's data. """
    lc = LushaClient(os.environ['LUSHA_TOKEN'])

    if not contact.direct or not contact.mobile:
        lc.enrich(contact)

    contact.patched = True
    contact.save()


def qualify_title(contact):
    """ Qualifies the contact's title. """
    if not contact.title:
        return

    ratings = [1, 2, 3]
    titles = [
        ['SENIOR VICE PRESIDENT', 'SVP', 'VICE PRESIDENT', 'VP',
        'PRESIDENT', 'CHIEF', 'DIRECTOR', 'HEAD', 'LEAD'],
        ['SENIOR MANAGER', 'MANAGER',
        'COORDINATOR', 'BUSINESS PARTNER'],
        ['ANALYST', 'GENERALIST',
        'ASSISTANT', 'SPECIALIST']]
    priorities = [1, 2, 3, 4, 5]
    functions = [
        'TALENT', 'RECRUIT', 'HIRING', 'HUMAN RESOURCES', 'HR']

    # title qualifier algorithm
    for group in titles:
        for title in group:
            if title in contact.title.upper():
                contact.rating = ratings[titles.index(group)]
                break

    # function qualifier algorithm
    for function in functions:
        if function in contact.title.upper():
            contact.priority = priorities[functions.index(function)]
            break

    contact.save()


def complete_account(account):
    sf = SalesforceClient(
        username=os.environ['SF_USERNAME'],
        password=os.environ['SF_PASSWORD'],
        security_token=os.environ['SF_TOKEN'],
        organizationId=os.environ['SF_ORG_ID'])

    sf.complete_account(account)
    account.delete()


def complete_contact(contact):
    sf = SalesforceClient(
        username=os.environ['SF_USERNAME'],
        password=os.environ['SF_PASSWORD'],
        security_token=os.environ['SF_TOKEN'],
        organizationId=os.environ['SF_ORG_ID'])

    if contact.ctype == 'old':
        sf.update_contact(contact)
    elif contact.ctype == 'new':
        sf.create_contact(contact)

    contact.delete()


def update_object(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if data(field.name):
            setattr(obj, field.name, data(field.name))

    obj.save()

