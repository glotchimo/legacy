"""
api.utils
~~~~~~~~~

This module implements utility methods for the API.
"""

# pylint:disable=E1101


def update_object(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if field.name in data and data[field.name]:
            setattr(obj, field.name, data[field.name])

    obj.save()
