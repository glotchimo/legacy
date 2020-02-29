"""
api.views
~~~~~~~~~

This module implements the endpoint methods for the API.
"""

# pylint:disable=E1101

import json

from api.utils import update_object

from django import http
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from satellites.decorators import auth_required, cors_enabled


@csrf_exempt
@cors_enabled
@auth_required
def get(request, model_name):
    module = __import__("api.models", fromlist=[model_name])
    model = getattr(module, model_name)

    params = request.GET.dict()

    if params:
        items = model.objects.filter(**params)
    else:
        items = model.objects.all()
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
def create(request, model_name):
    body = json.loads(request.body)

    parent_name = body["parent"]
    del body["parent"]

    parent_module = __import__("api.models", fromlist=[parent_name])
    parent_model = getattr(parent_module, parent_name)

    module = __import__("api.models", fromlist=[model_name])
    model = getattr(module, model_name)

    parent = parent_model.objects.get(id=body["pid"])
    del body["pid"]

    if body:
        body[parent_name.lower()] = parent
        model.objects.create(**body)
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
def update(request, model_name, id):
    module = __import__("api.models", fromlist=[model_name])
    model = getattr(module, model_name)

    try:
        item = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return http.HttpResponseNotFound()

    data = json.loads(request.body)
    update_object(item, data)

    item = model.objects.filter(id=id)
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
def delete(request, model_name, id):
    module = __import__("api.models", fromlist=[model_name])
    model = getattr(module, model_name)

    model.objects.get(id=id).delete()

    response = http.HttpResponse()
    response.content = b"Object deleted successfully."
    response.status_code = 200
    response["Access-Control-Allow-Origin"] = "*"

    return response
