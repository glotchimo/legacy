"""
app.utils
~~~~~~~~~

This module implements the utility methods for ax-s.

:copyright: (c) 2019 by Elliott Maguire
"""


def update(obj, data):
    """ Iterates through object attributes and updates values. """
    for field in obj._meta.fields:
        if data(field.name):
            setattr(obj, field.name, data(field.name))

    return obj

