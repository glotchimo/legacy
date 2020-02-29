"""
app.crons
~~~~~~~~~

This module implements the cron jobs for Pathfindr.

:copyright: (c) 2018 by Elliott Maguire
"""

import re

from django_cron import CronJobBase, Schedule

from app.models import Account, Contact
from app.utils import (
    SalesforceClient,
    LushaClient,
    DiscoverOrgClient)


class Sync(CronJobBase):
    """ Sync data with Salesforce. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.crons.Sync'

    def do(self):
        print('Syncing database...')

        sf_client = SalesforceClient()

        accounts = Account.objects.filter(
            status='queued')
        for account in accounts:
            contacts = Contact.objects.filter(
                account=account,
                status='queued')

            for contact in contacts:
                sf_client.create_contact(account, contact)
                contact.status = 'done'
                contact.save()
            
            sf_client.complete_account(account)
            account.status = 'done'
            account.save()
        

class Flush(CronJobBase):
    """ Flush database. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.crons.Flush'

    def do(self):
        print('Flushing database...')

        Account.objects.filter(status='done').delete()


class RefreshAccounts(CronJobBase):
    """ Refresh accounts. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.crons.RefreshAccounts'

    def do(self):
        print('Refreshing accounts...')

        sf_client = SalesforceClient()

        accounts = sf_client.get_accounts()
        for account in accounts:
            if not account['name'] or not account['domain']:
                continue
            
            obj, created = Account.objects.get_or_create(
                sfid=account['sfid'])

            if created:
                account['status'] = 'enrich'
            else:
                account['status'] = obj.status

            Account.objects.filter(pk=obj.pk).update(**account)


class RefreshContacts(CronJobBase):
    """ Refresh contacts. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.crons.RefreshContacts'

    def do(self):
        print('Refreshing contacts...')

        sf_client = SalesforceClient()
        dorg_client = DiscoverOrgClient()

        accounts = Account.objects.all()
        for account in accounts:
            sf_contacts = sf_client.get_contacts(account)
            dorg_contacts = dorg_client.search(account)

            if sf_contacts and dorg_contacts:
                contacts = sf_contacts + dorg_contacts
            elif sf_contacts and not dorg_contacts:
                contacts = sf_contacts
            elif dorg_contacts and not sf_contacts:
                contacts = dorg_contacts
            else:
                contacts = []

            for contact in contacts:
                obj, created = Contact.objects.get_or_create(
                    account=account,
                    name=contact['name'])

                if created:
                    contact['status'] = 'enrich'
                else:
                    contact['status'] = obj.status
                
                Contact.objects.filter(pk=obj.pk).update(**contact)

