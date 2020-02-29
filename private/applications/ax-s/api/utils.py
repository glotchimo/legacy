"""
api.utils
~~~~~~~~~

This module implements the utility methods for the ax-s API.

:copyright: 2019 by Elliott Maguire
"""

import sys
import json
import types
import xmltodict

from api.models import Error

from django.http import HttpResponse, JsonResponse

import requests


def call(request, api, endpoint):
    """ Call endpoint.

    :param request: the active request
    :param api: the requested API (an API object)
    :param endpoint: the requested endpoint (an Endpoint object)
    """
    url = ''.join([api.base, endpoint.path])
    method = endpoint.METHODS[endpoint.method - 1][1]

    r_data = json.loads(request.body) if request.body else None

    kwargs = {
        'headers': {
            **(json.loads(endpoint.headers)),
            **(r_data['headers'] if r_data and 'headers' in r_data else {})},
        'params': {
            **(json.loads(endpoint.params)),
            **(r_data['params'] if r_data and 'params' in r_data else {})},
        'data': {
            **(json.loads(endpoint.body)),
            **(r_data['body'] if r_data and 'body' in r_data else {})}}

    try:
        r = getattr(requests, method.lower())(url, **kwargs)
    except:
        return err(sys.exc_info(), api=api, endpoint=endpoint)

    if json.loads(endpoint.targets):
        try:
            data = parse(r, targets=endpoint.targets)
        except:
            return err(sys.exc_info())
        else:
            return JsonResponse(data=data)

    response = HttpResponse(content=r.text, status=r.status_code)

    restricted = (
        'Connection', 'Keep-Alive', 'Proxy-Authenticate',
        'Proxy-Authorization', 'TE', 'Trailers', 'Content-Length',
        'Transfer-Encoding', 'Content-Encoding', 'Upgrade')
    for k, v in r.headers.items():
        if k not in restricted:
            response[k] = v

    return response


def parse(response, targets):
    """ Parse response data.

    :param response: a requests.Response object
    :param targets: a list of data targets
    """
    targets = json.loads(targets) if targets else None

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        data = xmltodict.parse(response.text)

    if type(data) is list:
        data = {'data': data}

    output = {}
    def search(d):
        """ Searches a dictionary. """
        for k, v in d.items():
            if k in targets:
                output[k] = None
                yield v
            elif type(v) is dict:
                for i in v:
                    if i in targets:
                        output[i] = None
                        yield v[i]
                    elif type(v[i]) is dict:
                        for j in search(i):
                            output[j] = None
                            yield j

    for k, v in zip(output, [i for i in search(data)]):
        output[k] = v

    return output


def res(msg, status):
    """ Returns a qualified error response. """
    return HttpResponse(msg, status=status)


def err(info, api=None, endpoint=None):
    """ Store and return an internal server error. """
    Error.objects.create(
        api=api,
        endpoint=endpoint,
        traceback=info)

    return HttpResponse('Unknown error occurred.', status=500)


def update(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if data(field.name):
            setattr(obj, field.name, data(field.name))

    return obj

