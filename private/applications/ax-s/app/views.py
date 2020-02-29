"""
app.views
~~~~~~~~~

This module implements the web views for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

import json
import uuid

from app.utils import update
from app.models import Profile
from api.models import API, Endpoint

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def index(request):
    """ Landing view. (/) """
    return render(request, 'index.html')


def about(request):
    """ About view. (about) """
    return render(request, 'about.html')


def docs(request):
    """ Documentation. (docs) """
    return render(request, 'docs.html')


def terms(request):
    """ Terms of service. (terms) """
    return render(request, 'terms.html')


def privacy(request):
    """ Privacy policy. (privacy) """
    return render(request, 'privacy.html')


def login(request):
    """ User log in. (login) """
    error = False

    if request.method == 'POST':
        view = request.POST.get

        user = authenticate(username=view('username'), password=view('password'))
        if user:
            auth_login(request, user)
            return redirect('app:apis')
        else:
            error = True

    context = {'error': error}
    return render(request, 'registration/login.html', context)


def logout(request, error=None):
    """ User log out. (logout) """
    auth_logout(request)
    return redirect('app:index')


def signup(request, error=None):
    """ New user sign-up. (signup) """
    if request.method == 'POST':
        view = request.POST.get

        if view('password') != view('confirmation'):
            context = {'error': True}
            return render(request, 'registration/signup.html', context)

        user = User.objects.create_user(
            view('username'),
            email=view('email'),
            password=view('password'),
            first_name=view('first'),
            last_name=view('last'))

        profile = Profile.objects.create(user=user, token=uuid.uuid4().hex)

        text = (
            open('app/templates/registration/email.txt', 'r').read()
            .format(name=user.username, token=profile.token))
        html = (
            open('app/templates/registration/email.html', 'r').read()
            .format(name=user.username, token=profile.token))

        subject, from_email, to = 'new ax-s token', settings.DEFAULT_FROM_EMAIL, user.email
        msg = EmailMultiAlternatives(subject, text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()

        user = authenticate(username=view('username'), password=view('password'))
        auth_login(request, user)

        return redirect('app:apis')

    return render(request, 'registration/signup.html')


@login_required
def profile(request):
    """ User profile. (profile) """
    if request.method == 'POST':
        user = request.user.get
        post = request.POST.get

        user.first_name = post('first') or user.first_name
        user.last_name = post('last') or user.last_name
        user.username = post('username') or user.username
        if check_password(post('oldpass'), user.password):
            user.password = make_password(post('newpass'))

        user.save()

    return render(request, 'profile.html')


@login_required
def apis(request):
    """ APIs list. (apis) """
    apis = API.objects.filter(user=request.user)

    context = {'apis': apis}
    return render(request, 'apis.html', context=context)


@login_required
def view(request, name):
    """ API view. (<str:name/) """
    try:
        api = API.objects.get(user=request.user, name=name)
    except ObjectDoesNotExist:
        return redirect('app:apis')
    except MultipleObjectsReturned:
        return redirect('app:apis')

    endpoints = Endpoint.objects.filter(api=api)

    context = {'api': api, 'endpoints': endpoints}
    return render(request, 'view.html', context)


@login_required
def edit(request, name):
    """ API edit. (<str:name>/edit) """
    api = API.objects.get(user=request.user, name=name)
    endpoints = Endpoint.objects.filter(api=api)
    if not api:
        context = {'permanent': True}
        return redirect('app:apis', **context)

    if request.method == 'POST':
        post = request.POST.get

        api = update(api, post)

        api.auth = 1 if post('auth') == 'None' else api.auth
        api.auth = 2 if post('auth') == 'Basic' else api.auth
        api.auth = 3 if post('auth') == 'Header' else api.auth
        api.auth = 4 if post('auth') == 'Params' else api.auth

        api.save()

    context = {'api': api, 'endpoints': endpoints}
    return render(request, 'edit.html', context)

