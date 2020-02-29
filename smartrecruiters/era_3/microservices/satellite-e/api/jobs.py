"""
api.jobs
~~~~~~~~

This module implements all recurring jobs.
"""

# pylint:disable=E1101

from datetime import datetime

from api import utils
from api.models import Account, Contact
from api.clients import SalesforceClient, DiscoverOrgClient

from django_cron import CronJobBase, Schedule

from progress.bar import Bar


class Upload(CronJobBase):
    """ Uploads queued records into Salesforce. """

    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.jobs.Upload"

    def do(self):
        sf = SalesforceClient()

        accounts = Account.objects.filter(status="upload")
        bar = Bar("RECORD UPLOAD", max=accounts.count())
        for account in accounts:
            old = Contact.objects.filter(
                account=account, status="upload", ctype="old", cleaned=True
            )
            sf.update_contacts(old)

            new = Contact.objects.filter(account=account, status="upload", ctype="new")
            sf.create_contacts(new)

            bar.next()

        completed = Account.objects.filter(cleaned=True, enriched=True)
        if completed:
            sf.complete_accounts(completed)

        bar.finish()


class SyncAccounts(CronJobBase):
    """ Sync accounts with Salesforce. """

    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.jobs.SyncAccounts"

    def do(self):
        sf = SalesforceClient()

        accounts = sf.get_accounts()
        bar = Bar("ACCOUNT SYNC", max=len(accounts))
        for account in accounts:
            if not account["name"] or not account["domain"]:
                continue

            obj, created = Account.objects.get_or_create(sfid=account["sfid"])
            account["status"] = "enrich" if created else obj.status

            Account.objects.filter(pk=obj.pk).update(**account)

            bar.next()

        bar.finish()


class GetContacts(CronJobBase):
    """ Gets contacts for accounts from Salesforce. """

    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.jobs.GetContacts"

    def do(self):
        sf = SalesforceClient()
        do = DiscoverOrgClient()

        accounts = Account.objects.exclude(prep=None)
        bar = Bar("CONTACT COLLECTION", max=accounts.count())
        for account in accounts:
            sf_contacts = sf.get_contacts(account)

            if str(account.updated) != str(datetime.today().strftime("%Y-%m-%d")):
                do_contacts = do.get_contacts(account)
                account.updated = datetime.today().strftime("%Y-%m-%d")
                account.save()
            else:
                do_contacts = []

            contacts = sf_contacts + do_contacts
            for contact in contacts:
                obj, created = Contact.objects.get_or_create(
                    account=account, name=contact["name"]
                )
                contact["status"] = contact["status"] if created else obj.status
                contact["ctype"] = contact["ctype"] if created else obj.ctype

                Contact.objects.filter(pk=obj.pk).update(**contact)

            bar.next()

        bar.finish()


class QualifyContacts(CronJobBase):
    """ Qualifies and prioritizes contact titles. """

    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "api.jobs.QualifyContacts"

    def do(self):
        contacts = Contact.objects.all()
        bar = Bar("CONTACT QUALIFICATION", max=contacts.count())
        for contact in contacts:
            utils.qualify_title(contact)

            bar.next()

        bar.finish()
