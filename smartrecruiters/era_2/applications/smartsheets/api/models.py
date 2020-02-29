"""
api.models
~~~~~~~~~~

This module implements API models.
"""

from api.utils import get_session, get_status

from django.db import models
from django.contrib.auth.models import User


class ProjectManager(models.Manager):
    def create_project(self, user, url, worksheet):
        sheet, worksheet = get_session(url, worksheet)
        size, progress = get_status(worksheet)

        project = Project.objects.create(
            user=user,
            name=sheet.title,
            status='requested',
            url=url,
            gid=sheet.id,
            worksheet=worksheet.title,
            size=size,
            progress=progress)

        return project


class Project(models.Model):
    objects = ProjectManager()

    date_requested = models.DateField('Date Requested', auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField('Name', max_length=256, default='New Project')
    status = models.CharField('Status', max_length=32, default='requested')

    url = models.URLField('Sheet URL', null=True)
    gid = models.CharField('Google ID', max_length=128, null=True)
    worksheet = models.CharField('Worksheet Name', max_length=128, null=True)

    size = models.IntegerField('Size', null=True)
    progress = models.IntegerField('Progress', null=True)

    def __str__(self):
        return self.name

