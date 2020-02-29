"""
satellites.decorators
~~~~~~~~~~~~~~~~~~~~~

This module implements standard decorators for the Satellites.
"""

from .s import Security

from django.http import HttpResponse, HttpResponseForbidden


def cors_enabled(func):
    def decorator(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response.status_code = 200

            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = (
                'Origin, Content-Type, Authorization')

            return response
        else:
            return func(request, *args, **kwargs)

    decorator.__doc__ = func.__doc__
    decorator.__name__ = func.__name__

    return decorator


def auth_required(func):
    def decorator(request, *args, **kwargs):
        token = (
            request.headers['Authorization'].split()[1]
            if 'Authorization' in request.headers
            else '')

        security = Security()
        if not security.authorize(token):
            print(f"Authorization failed, invalid token: {token}.")
            return HttpResponseForbidden()
        else:
            return func(request, *args, **kwargs)

    decorator.__doc__ = func.__doc__
    decorator.__name__ = func.__name__

    return decorator
