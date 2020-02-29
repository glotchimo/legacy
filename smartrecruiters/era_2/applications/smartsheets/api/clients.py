"""
api.clients
~~~~~~~~~~~

This module implements external API clients.
"""

import os
import sys
import time
import json

import requests


class DiscoverOrgClient:
    """ Implements a DiscoverOrg API client. """
    def __init__(self):
        self.base = 'https://papi.discoverydb.com/papi'

        self.username = os.environ['DO_USERNAME']
        self.password = os.environ['DO_PASSWORD']
        self.key = os.environ['DO_KEY']

        self.token = self._get_token()


    def _get_token(self):
        """ Gets a session key.
        :return session: a session key
        """
        url = ''.join([self.base, '/login'])
        headers = {
            'Content-Type': 'application/json'}
        data = {
            'username': self.username,
            'password': self.password,
            'partnerKey': self.key}

        response = requests.post(url, headers=headers, data=json.dumps(data))
        token = response.headers['X-AUTH-TOKEN']

        return token

    def enrich(self, contact):
        """ Enriches a contact records. """
        url = ''.join([self.base, '/v1/search/persons'])
        headers = {
            'X-PARTNER-KEY': self.key,
            'X-AUTH-TOKEN': self.token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'}
        data = json.dumps({
            'personCriteria': {
                'queryString': f"{contact['First Name']} {contact['Last Name']}",
                'queryStringApplication': ['FULL_NAME']},
            'companyCriteria': {
                'queryString': f"{contact['Company']}",
                'queryStringApplication': ['NAME']}})

        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            return response.text

        data = json.loads(response.text)
        content = data['content']
        if content:
            record = content[0]
        else:
            return response.text

        contact['Direct Line'] = (
            record['officeTelNumber']
            if 'officeTelNumber' in record
            else contact['Direct Line'])
        contact['Mobile Line'] = (
            record['mobileTelNumber']
            if 'mobileTelNumber' in record
            else contact['Mobile Line'])
        contact['Email'] = (
            record['email']
            if 'email' in record
            else contact['Email'])

        if 'company' in record:
            contact['Company Size'] = (
                record['company']['numEmployees']
                if 'numEmployees' in record['company']
                else contact['Company Size'])
            contact['Industry'] = (
                record['company']['industry']
                if 'industry' in record['company']
                else contact['Industry'])

        contact['Confidence'] = 1/len(content)
        contact['Status'] = 'Completed'

        return contact

