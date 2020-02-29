import os
import sys
import time
import json
import random

from smartlib.api import SmartLibrary
from smartlib.exceptions import SmartRecruitersError

import requests
import names

BASE_URL = 'https://api.smartrecruiters.com'
SOURCE_DATA = json.loads(
    open('resource/candidate_data.json', 'r').read()
)


class Utility:
    """
    The Utility class abstracts all functions that enable the automation
    and intuition present in the CLI.
    """
    def __init__(self, instance={}):
        self.instance = instance

    def create_candidate_json(self):
        """ Generate JSON candidate object for API submission
        
        Returns:
            candidate_json -- JSON string of randomly generated candidate data

        """
        if self.instance['type'] == 'US':
            companies = SOURCE_DATA['companies_us']
            locations = SOURCE_DATA['locations_us']
        elif self.instance['type'] == 'EU':
            companies = SOURCE_DATA['companies_eu']
            locations = SOURCE_DATA['locations_eu']

        first_name = names.get_first_name()
        last_name = names.get_last_name()
        location = random.choice(locations)
        uni_start = random.randint(1980, 2000)
        work_start = uni_start + random.randint(3, 6)
        source = random.choice(SOURCE_DATA['sources'])
        candidate_dict = {
            'firstName': first_name,
            'lastName': last_name,
            'email': (first_name 
                     + '.' 
                     + last_name 
                     + str(random.randint(100, 9999))
                     + '@mailinator.com'),
            'phone': str(random.randint(1000000, 9999999)),
            'location': {
                'country': location[0],
                'countryCode': location[1],
                'regionCode': '',
                'region': location[4],
                'city': location[3],
                'address': '',
                'postalCode': ''
            },
            'web': {
                'skype': '',
                'linkedin': '',
                'facebook': '',
                'twitter': '',
                'website': ''
            },
            'tags': [random.choice(SOURCE_DATA['tags']) for _ in range(3)],
            'education': [
                {
                    'institution': random.choice(SOURCE_DATA['schools']),
                    'degree': 'B.A.',
                    'major': random.choice(SOURCE_DATA['majors']),
                    'current': False,
                    'location': '',
                    'startDate': str(uni_start),
                    'endDate': str(uni_start + random.randint(4, 6))
                }
            ],
            'experience': [
                {
                    'title': random.choice(SOURCE_DATA['titles']),
                    'company': random.choice(companies),
                    'current': True,
                    'startDate': str(work_start),
                    'endDate': str(work_start + 2),
                    'location': '',
                    'description': ', '.join(
                        [
                            random.choice(SOURCE_DATA['descriptions']) 
                            for _ in range(2)
                        ]
                    )
                },
                {
                    'title': random.choice(SOURCE_DATA['titles']),
                    'company': random.choice(companies),
                    'current': True,
                    'startDate': str(work_start + 2),
                    'endDate': str(work_start + 4),
                    'location': '',
                    'description': ', '.join(
                        [
                            random.choice(SOURCE_DATA['descriptions']) 
                            for _ in range(2)
                        ]
                    )
                },
                {
                    'title': random.choice(SOURCE_DATA['titles']),
                    'company': random.choice(companies),
                    'current': True,
                    'startDate': str(work_start + 4),
                    'endDate': str(work_start + 6),
                    'location': '',
                    'description': ', '.join(
                        [
                            random.choice(SOURCE_DATA['descriptions']) 
                            for _ in range(2)
                        ]
                    )
                }
            ],
            'sourceDetails': {
                'sourceTypeId': source[0],
                'sourceId': source[1]
            }
        }

        candidate_json = json.dumps(candidate_dict)

        return candidate_json


    def _get_instance(self, token):
        """
        Get and return instance data from the configuration API
        using the given SmartToken.

        Arguments:
            token -- a SmartToken string

        Returns:
            instance -- a dictionary of SR instance information
        """
        endpoint = '/configuration/company'
        headers = {
            'X-SmartToken': token
        }

        response = requests.get(
            BASE_URL + endpoint,
            headers=headers
        )

        try:
            response.text
        except AttributeError:
            raise ValueError(requests.Response)
        else:
            try:
                instance = json.loads(response.text)
            except ValueError:
                raise ValueError(requests.Response)
            else:
                try:
                    instance['name']
                except KeyError:
                    raise SmartRecruitersError(
                        BASE_URL + endpoint,
                        400,
                        endpoint,
                        instance
                    )
                else:
                    if instance['location']['country'] == 'United States':
                        instance['type'] = 'US'
                    else:
                        instance['type'] = 'EU'

                    return instance

    def _list_tokens(self):
        """
        Get and return all saved SmartTokens from tokens.txt

        Returns:
            tokenlist -- a list of SmartTokens

        """
        try:
            token_file = open('smarty/resource/tokens.txt', 'r')
        except IOError: # create the file if it doesn't exist yet
            open('smarty/resource/tokens.txt', 'w+')
            token_file = open('smarty/resource/tokens.txt', 'r')

        tokenlist = []
        for line in token_file.readlines():
            vals = line.split(' | ')
            tokenlist.append([vals[0], vals[1]])

        return tokenlist

    def _save_token(self, token, name):
        """
        Save a token and its instance name in tokens.txt

        Arguments:
            token -- a string SmartToken
            name -- a name for the token (the instance name)

        """
        try:
            token_file = open('smarty/resource/tokens.txt', 'a')
        except IOError: # create the file if it doesn't exist yet
            open('smarty/resource/tokens.txt', 'w+')
            token_file = open('smarty/resource/tokens.txt', 'a')
        
        token_file.write(
            name + ' | ' + token
        )