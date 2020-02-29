"""
satellites.s
~~~~~~~~~~~~

This module implements the client for satellite-s (security).
"""

import requests


class Security:
    def __init__(self):
        self.base = 'https://s.satellites.smartian.space'

    def create_user(self, data):
        """ Creates a user. """
        url = ''.join([self.base, f"/create"])

        response = requests.post(url, data=data)

        return response

    def confirm_user(self, username, cid):
        """ Confirms a user. """
        url = ''.join([self.base, f"/confirm"])
        params = {
            'username': username,
            'cid': cid}

        response = requests.get(url, params=params)

        return response

    def get_users(self, token, username=None):
        """ Gets a user by username and token. """
        url = ''.join([self.base, f"/get"])
        headers = {'Authorization': f"Basic {token}"}
        if username:
            headers['x-username'] = username

        response = requests.get(url, headers=headers)

        return response

    def authenticate(self, username, password):
        """ Authenticates with username and password, returns access token. """
        url = ''.join([self.base, f"/authenticate"])
        headers = {
            'x-username': username,
            'x-password': password}

        response = requests.get(url, headers=headers)

        return response

    def authorize(self, token):
        """ Authorizes by token. """
        url = ''.join([self.base, f"/authorize"])
        headers = {'Authorization': f"Basic {token}"}

        response = requests.get(url, headers=headers)

        return response
