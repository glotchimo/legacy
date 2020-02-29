"""
api.jobs
~~~~~~~~

This module implements all recurring jobs.
"""

# pylint:disable=E1101

from api import utils
from api.models import Page

from django_cron import CronJobBase, Schedule


class UpdatePages(CronJobBase):
    run_at_times = ["00:00"]

    schedule = Schedule(run_at_times=run_at_times)
    code = "api.jobs.UpdatePages"

    def do(self):
        print("api.jobs: PAGE UPDATE STARTED")

        pages = Page.objects.all()
        for page in pages:
            page.update()
