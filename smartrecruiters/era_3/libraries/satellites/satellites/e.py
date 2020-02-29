"""
satellites.e
~~~~~~~~~~~~

This module implements the client for satellite-e (enrichment).
"""

import requests


class Enrichment:
    def __init__(self, token):
        self.base = 'https://e.satellites.smartian.space'
        self.token = token

    def get_accounts(self, params=None):
        """ Gets a list of active accounts. """
        url = ''.join([self.base, f"/accounts"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.get(
            url, headers=headers, params=params)

        return response

    def create_account(self, data):
        """ Creates an account. """
        url = ''.join([self.base, f"/accounts/create"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def update_account(self, id, data):
        """ Updates an account by Salesforce ID. """
        url = ''.join([self.base, f"/accounts/{id}/update"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def delete_account(self, id):
        """ Deletes an account from the satellite database. """
        url = ''.join([self.base, f"/accounts/{id}/remove"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.delete(url, headers=headers)

        return response

    def get_contacts(self, params):
        """ Gets a list of contacts based on parameters. """
        url = ''.join([self.base, f"/contacts"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.get(url, headers=headers, params=params)

        return response

    def create_contact(self, data):
        """ Creates a new contact. """
        url = ''.join([self.base, f"/contacts/create"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def update_contact(self, id, data):
        """ Updates a contact by ID. """
        url = ''.join([self.base, f"/contacts/{id}/update"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.post(url, headers=headers, data=data)

        return response

    def delete_contact(self, id):
        """ Deletes a contact. """
        url = ''.join([self.base, f"/contacts/{id}/delete"])
        headers = {'Authorization': f"Basic {self.token}"}

        response = requests.delete(url, headers=headers)

        return response
