"""
api.jobs
~~~~~~~~

This module implements recurring jobs.
"""

import os
import re
import time

from api.models import Project
from api.clients import DiscoverOrgClient
from api.utils import get_session, get_status

from django_cron import CronJobBase, Schedule


class Sync(CronJobBase):
    """ Syncs project meta from sources. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.Sync'

    def do(self):
        print('Syncing projects...')

        projects = Project.objects.all()
        for project in projects:
            sheet, worksheet = get_session(project.url, project.worksheet)
            size, progress = get_status(worksheet)

            project.size = size
            project.progress = progress

            project.save()


class Enrich(CronJobBase):
    """ Enriches contacts in all projects. """
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.jobs.Enrich'

    def do(self):
        print('Enriching projects...')

        do = DiscoverOrgClient()

        projects = Project.objects.filter(status='running bots')
        for project in projects:
            sheet, worksheet = get_session(project.url, project.worksheet)

            contacts = worksheet.get_all_records()
            for contact in contacts:
                if contact['Status'] != 'Completed':
                    contact = do.enrich(contact)
                    if type(contact) is str:
                        continue
                else:
                    continue

                for k, v in contact.items():
                    row = contacts.index(contact) + 2
                    col = worksheet.find(k).col

                    worksheet.update_cell(row, col, v)

                    time.sleep(1)

                time.sleep(3)

            project.status = 'in progress'
            project.save()

