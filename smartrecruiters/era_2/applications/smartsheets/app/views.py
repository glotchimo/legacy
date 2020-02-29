"""
app.views
~~~~~~~~~

This module implements the app views.

:copyright: (c) 2019 by Elliott Maguire
"""

from api.models import Project

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    """ Home page. """
    return render(request, 'index.html')


def signup(request, error=None):
    """ New user sign-up. (signup) """

    # Handle POST submission.
    if request.method == 'POST':
        # Restate POST data.
        post = request.POST.get

        # Confirm password
        if post('password') != post('confirmation'):
            context = {'error': True}
            return render(request, 'registration/signup.html', context)

        # Build and save new user.
        user = User.objects.create_user(
            post('username'),
            email=post('email'),
            password=post('password'),
            first_name=post('first'),
            last_name=post('last'))

        # Authenticate and log user in.
        user = authenticate(username=post('username'), password=post('password'))
        login(request, user)

        return redirect('app:projects')

    return render(request, 'registration/signup.html')


@login_required
def projects(request):
    """ Projects page. """
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=request.user)

    context = {
        'projects': projects,
        'requested': projects.filter(status='requested').count(),
        'completed': projects.filter(status='completed').count()}

    return render(request, 'projects.html', context)

