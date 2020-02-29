"""
api.jobs
~~~~~~~~

This module implements the recurring jobs.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import utils
from api.models import Account, Contact
from api.clients import SalesforceClient, LushaClient, DiscoverOrgClient

from django_cron import CronJobBase, Schedule


class Sync(CronJobBase):
    """ Uploads queued records into Salesforce. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.Sync'

    def do(self):
        print('api.jobs: RECORD SYNC STARTED')

        for account in Account.objects.filter(status='upload'):
            contacts = Contact.objects.filter(
                account=account,
                status='upload')
            for contact in contacts:
                if not contact.patched:
                    utils.enrich_contact(contact)

                if contact.ctype == 'new':
                    utils.complete_contact(contact)
                elif contact.ctype == 'old' and contact.cleaned:
                    utils.complete_contact(contact)

            if account.cleaned and account.enriched:
                utils.complete_account(account)


class GetAccounts(CronJobBase):
    """ Get accounts from Salesforce. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.GetAccounts'

    def do(self):
        print('api.jobs: ACCOUNT COLLECTION STARTED')

        sf = SalesforceClient()

        for account in sf.get_accounts():
            if not account['name'] or not account['domain']:
                continue

            obj, created = Account.objects.get_or_create(
                sfid=account['sfid'])
            account['status'] = 'enrich' if created else obj.status

            Account.objects.filter(pk=obj.pk).update(**account)


class GetContacts(CronJobBase):
    """ Gets contacts for accounts from Salesforce. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.GetContacts'

    def do(self):
        print('api.jobs: CONTACT COLLECTION STARTED')

        sf = SalesforceClient()

        dg = DiscoverOrgClient()

        for account in Account.objects.all():
            sf_contacts = sf.get_contacts(account) or []
            do_contacts = dg.get_contacts(account) or []
            contacts = sf_contacts + do_contacts

            for contact in contacts:
                obj, created = Contact.objects.get_or_create(
                    account=account,
                    name=contact['name'])
                contact['status'] = contact['status'] if created else obj.status
                contact['ctype'] = contact['ctype'] if created else obj.ctype

                Contact.objects.filter(pk=obj.pk).update(**contact)


class QualifyContacts(CronJobBase):
    """ Qualifies and prioritizes contact titles. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.QualifyContacts'

    def do(self):
        print('api.jobs: CONTACT QUALIFICATION STARTED')

        contacts = Contact.objects.all()
        for contact in contacts:
            utils.qualify_title(contact)
