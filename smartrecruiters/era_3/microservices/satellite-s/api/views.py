"""
api.views
~~~~~~~~~

This module implements the endpoint methods for the API.
"""

# pylint:disable=E1101

import json
import secrets
import uuid

from api.models import Profile
from api.decorators import cors_enabled

from django import http
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


@csrf_exempt
@cors_enabled
def create_user(request):
    data = json.loads(request.body)

    if "@smartrecruiters.com" not in data["email"]:
        return http.HttpResponseForbidden()

    user = User.objects.create_user(
        data["email"],
        email=data["email"],
        password=data["password"],
        first_name=data["first_name"],
        last_name=data["last_name"],
    )
    profile = Profile.objects.create(
        user=user,
        cid=uuid.uuid4().hex,
        sfid=data["sfid"],
        token=secrets.token_urlsafe(),
    )

    text = (
        open("api/templates/email.txt", "r")
        .read()
        .format(name=user.username, username=user.username, cid=profile.cid)
    )
    html = (
        open("api/templates/email.html", "r")
        .read()
        .format(name=user.username, username=user.username, cid=profile.cid)
    )

    subject, from_email, to = (
        "Confirm your Smartian Space account",
        settings.DEFAULT_FROM_EMAIL,
        user.email,
    )
    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()

    response = http.HttpResponse()
    response.content = b"User created successfully."
    response.status_code = 200
    response["Authorization"] = profile.token

    return response


def confirm_user(request):
    get = request.GET.get

    user = User.objects.get_by_natural_key(get("username"))
    profile = Profile.objects.get(user=user)

    if get("cid") != profile.cid:
        return http.HttpResponseForbidden()

    profile.status = "confirmed"
    profile.save()

    return redirect("https://hub.smartian.space")


def get_users(request):
    if "X-Username" in request.headers:
        user = User.objects.get_by_natural_key(request.headers["X-Username"])
        profiles = Profile.objects.filter(user=user)

        if profiles[0].token not in request.headers["Authorization"]:
            return http.HttpResponseForbidden()
    else:
        profiles = Profile.objects.all()
        tokens = Profile.objects.values_list("token", flat=True)

        if request.headers["Authorization"].split()[1] not in tokens:
            return http.HttpResponseForbidden()

    data = serializers.serialize("json", profiles)

    response = http.HttpResponse()
    response.content = data
    response.content_type = "application/json"
    response.status_code = 200

    return response


def authenticate(request):
    user = User.objects.get_by_natural_key(request.headers["X-Username"])
    profile = Profile.objects.get(user=user)

    if not check_password(request.headers["X-Password"], user.password):

        return http.HttpResponseForbidden()

    response = http.HttpResponse()
    response.status_code = 200
    response["X-Token"] = f"{profile.token}"

    return response


def authorize(request):
    headers = request.headers
    token = headers["Authorization"].split()[1]

    profile = Profile.objects.filter(token=token).count()
    if not profile:
        return http.HttpResponseForbidden()

    response = http.HttpResponse()
    response.status_code = 200

    return response
