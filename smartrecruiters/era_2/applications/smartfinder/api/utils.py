"""
api.utils
~~~~~~~~~

This module implements the utility methods.

:copyright: (c) 2019 by Elliott Maguire
"""

import os
import sys

from api.models import Account, Contact, ErrorLog
from api.clients import SalesforceClient, DiscoverOrgClient, LushaClient


def get_hierarchy(account):
    """ Gets the org chart for a given account. """
    do = DiscoverOrgClient()

    hierarchy = do.get_hierarchy(account)

    return hierarchy


def enrich_contact(contact):
    """ Enriches a contact's data. """
    lc = LushaClient()

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
    sf = SalesforceClient()

    sf.complete_account(account)

    account.delete()


def complete_contact(contact):
    sf = SalesforceClient()

    if contact.ctype == 'new':
        try:
            sf.create_contact(contact)
            contact.delete()
        except:
            ErrorLog.objects.create(traceback=sys.exc_info())

            contact.status = 'hold'
            contact.save()
    elif contact.ctype == 'old' and contact.cleaned:
        try:
            sf.update_contact(contact)
            contact.delete()
        except:
            ErrorLog.objects.create(traceback=sys.exc_info())

            contact.status = 'hold'
            contact.save()


def update_object(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if data(field.name):
            setattr(obj, field.name, data(field.name))

    obj.save()
