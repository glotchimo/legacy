"""
api.views
~~~~~~~~~

This module implements API endpoints.
"""

from api.models import Project

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def create_project(request):
    """ Creates a new project request. """
    if request.method != 'POST':
        return HttpResponse(content='Invalid request.', status=405)
    else:
        post = request.POST.get

    try:
        Project.objects.create_project(
            user=request.user,
            url=post('url'),
            worksheet=post('worksheet'))
    except:
        print('Failed to fetch sheet.')

    return redirect('app:projects')


@login_required
def mark_project(request, pid, status):
    """ Marks a project with a given status. """
    project = Project.objects.get(id=pid)

    project.status = status
    project.save()

    return redirect('app:projects')


@login_required
def delete_project(request, pid):
    """ Deletes a given project. """
    Project.objects.get(id=pid).delete()

    return redirect('app:projects')

