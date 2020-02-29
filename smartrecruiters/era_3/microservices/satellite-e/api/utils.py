"""
api.utils
~~~~~~~~~

This module implements utility methods for the API.
"""

# pylint:disable=E1101

import requests


def authorize(auth):
    """ .Checks an access token through satellite-s """
    url = "https://security.smartian.space/authorize"
    headers = {"Authorization": auth}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False


def qualify_title(contact):
    """ Qualifies the contact's title. """
    if not contact.title:
        return

    ratings = [1, 2, 3]
    titles = [
        [
            "SENIOR VICE PRESIDENT",
            "SVP",
            "VICE PRESIDENT",
            "VP",
            "PRESIDENT",
            "CHIEF",
            "DIRECTOR",
            "HEAD",
            "LEAD",
        ],
        ["SENIOR MANAGER", "MANAGER", "COORDINATOR", "BUSINESS PARTNER"],
        ["ANALYST", "GENERALIST", "ASSISTANT", "SPECIALIST"],
    ]
    priorities = [1, 2, 3, 4, 5]
    functions = ["TALENT", "RECRUIT", "HIRING", "HUMAN RESOURCES", "HR"]

    # title qualifier algorithm
    for group in titles:
        for title in group:
            if title in contact.title.upper():
                contact.rating = ratings[titles.index(group)]
                break

    # function qualifier algorithm
    for function in functions:
        if function in contact.title.upper():
            contact.priority = priorities[functions.index(function)]
            break

    contact.save()


def update_object(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if field.name in data and data[field.name]:
            setattr(obj, field.name, data[field.name])

    obj.save()
