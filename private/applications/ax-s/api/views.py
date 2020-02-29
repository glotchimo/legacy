"""
api.views
~~~~~~~~~

This module implements the API routes for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""

import sys

from api.utils import call, parse, res, err, update
from api.models import API, Endpoint, Error
from app.models import Profile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def caller(request, token):
    """ Parse a request to call an endpoint. """
    if not request.method == 'POST':
        return res(
            'Method not allowed; must be POST.',
            status=405)

    try:
        auth = request.META['HTTP_AUTHORIZATION'].split()[1]
    except KeyError:
        return res(
            'Unauthorized. Please provide an access token.',
            status=401)
    except:
        return err(sys.exc_info())

    try:
        profile = Profile.objects.get(token=auth)
        user = profile.user
    except ObjectDoesNotExist:
        return res(
            'Unauthorized. Invalid access token.',
            status=401)
    except:
        return err(sys.exc_info())

    try:
        api = API.objects.get(user=user, token=token)
    except ObjectDoesNotExist:
        return res(
            'No API found. Verify token and try again.',
            status=404)
    except:
        return err(sys.exc_info())

    try:
        name = request.GET.get('endpoint')
        endpoint = Endpoint.objects.get(api=api, name=name)
    except ObjectDoesNotExist:
        return res(
            'No endpoint found. Verify name and try again.',
            status=404)
    except:
        return err(sys.exc_info(), api=api)

    return call(request, api, endpoint)


@login_required
def api_add(request):
    """ API add. (add) """
    api = API.objects.create_api(user=request.user)

    context = {'name': api.name}
    return redirect('app:view', **context)


@login_required
def api_delete(request, name):
    """ API delete. (<str:name>/delete) """
    API.objects.get(user=request.user, name=name).delete()

    return redirect('app:apis')


@login_required
def endpoint_add(request, name):
    """ Endpoint add. (<str:name>/add) """
    api = API.objects.get(name=name)
    Endpoint.objects.get_or_create(
        api=api,
        name='New Endpoint',
        path='path/from/base',
        method=1)

    context = {'name': api.name}
    return redirect('app:edit', **context)


@login_required
def endpoint_edit(request, name, endpoint):
    """ Endpoint edit. (<str:name>/<str:endpoint) """
    api = API.objects.get(user=request.user, name=name)
    endpoint = Endpoint.objects.get(api=api, name=endpoint)

    if request.method == 'POST':
        post = request.POST.get

        endpoint = update(endpoint, post)

        endpoint.method = 1 if post('method') == 'GET' else 1
        endpoint.method = 2 if post('method') == 'POST' else 1
        endpoint.method = 3 if post('method') == 'PUT' else 1
        endpoint.method = 4 if post('method') == 'PATCH' else 1
        endpoint.method = 5 if post('method') == 'DELETE' else 1

        endpoint.auth = True if post('method') == 'on' else False

        endpoint.save()

        context = {'name': api.name}
        return redirect('app:edit', **context)

    return render(request, 'endpoint.html')


@login_required
def endpoint_delete(request, name, endpoint):
    """ Endpoint delete. (<str:name>/<str:endpoint>/delete) """
    api = API.objects.get(user=request.user, name=name)
    Endpoint.objects.get(api=api, name=endpoint).delete()

    context = {'name': api.name}
    return redirect('app:edit', **context)

