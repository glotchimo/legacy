"""
api.views
~~~~~~~~~

This module implements the endpoint methods for the API.
"""

# pylint:disable=E1101

import json

from api.models import Account, Contact
from api.utils import update_object

from django import http
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from satellites.decorators import auth_required, cors_enabled


@csrf_exempt
@cors_enabled
@auth_required
def get_accounts(request):
    params = request.GET.dict()

    if params:
        items = Account.objects.filter(**params)
    else:
        items = Account.objects.all()
    data = serialize("json", items)

    response = http.HttpResponse()
    response.content = data
    response.content_type = "application/json"
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def create_account(request):
    body = json.loads(request.body)

    if body:
        Account.objects.create(**body)
    else:
        return http.HttpResponseBadRequest()

    response = http.HttpResponse()
    response.content = b"Object created successfully."
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def update_account(request, id):
    try:
        item = Account.objects.get(id=id)
    except ObjectDoesNotExist:
        return http.HttpResponseNotFound()

    data = json.loads(request.body)
    update_object(item, data)

    item = Account.objects.filter(id=id)
    data = serialize("json", item)

    response = http.HttpResponse()
    response.content = data
    response.content_type = "application/json"
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def delete_account(request, id):
    Account.objects.get(id=id).delete()

    response = http.HttpResponse()
    response.content = b"Object deleted successfully."
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def get_contacts(request):
    params = request.GET.dict()

    if params:
        items = Contact.objects.filter(**params)
    else:
        items = Contact.objects.all()
    data = serialize("json", items)

    response = http.HttpResponse()
    response.content = data
    response.content_type = "application/json"
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def create_contact(request):
    body = json.loads(request.body)

    account = Account.objects.get(id=body["pid"])
    del body["pid"]

    if "name" not in body:
        body["name"] = "New Contact"

    if body:
        body["account"] = account
        Contact.objects.create(**body)
    else:
        return http.HttpResponseBadRequest()

    response = http.HttpResponse()
    response.content = b"Object created successfully."
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def update_contact(request, id):
    try:
        item = Contact.objects.get(id=id)
    except ObjectDoesNotExist:
        return http.HttpResponseNotFound()

    data = json.loads(request.body)
    update_object(item, data)

    item = Contact.objects.filter(id=id)
    data = serialize("json", item)

    response = http.HttpResponse()
    response.content = data
    response.content_type = "application/json"
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@cors_enabled
@auth_required
def delete_contact(request, id):
    Contact.objects.get(id=id).delete()

    response = http.HttpResponse()
    response.content = b"Object deleted successfully."
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response
