"""
satellites.spy
~~~~~~~~~~~~~~

This module implements the client for satellite-e (enrichment).
"""

import requests


class Spy:
    def __init__(self, token):
        self.base = 'https://spy.satellites.smartian.space/api'
        self.token = token

    def get(self, model, params=None):
        """ Gets a list of properties based on parameters. """
        url = ''.join([self.base, f"/{model}"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.get(url, headers=headers, params=params)

        return response

    def create(self, parent, model, data):
        """ Creates a new property. """
        url = ''.join([self.base, f"/{parent}/{model}/create"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def update(self, model, id, data):
        """ Updates a property by ID. """
        url = ''.join([self.base, f"/{model}/{id}/update"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def delete(self, model, id):
        """ Deletes a property by ID. """
        url = ''.join([self.base, f"/{model}/{id}/delete"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.delete(url, headers=headers)

        return response
