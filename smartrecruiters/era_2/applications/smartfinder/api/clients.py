"""
api.clients
~~~~~~~~~~~

This module implements the API clients.

:copyright: (c) 2019 by Elliott Maguire, SmartRecruiters
"""

import os
import sys
import time
import json

from api.models import Account, Contact, ErrorLog

import requests
import simple_salesforce


class SalesforceClient:
    """ Client for the Salesforce API. """

    def __init__(self):
        self.api = simple_salesforce.Salesforce(
            username=os.environ['SF_USERNAME'],
            password=os.environ['SF_PASSWORD'],
            security_token=os.environ['SF_TOKEN'],
            organizationId=os.environ['SF_ORG_ID'])

    def get_accounts(self):
        """ Collects enrichment requests from Salesforce.

        :return accounts: a list of dictionaries of account data
        """
        sql = """
            SELECT
                Id, DSCORGPKG__DiscoverOrg_ID__c, Name, Phone, Website,
                Enrichment_Requested_By__c, Enrichment_Requested_Date__c
            FROM
                Account
            WHERE
                Enrichment_Requested__c = True
            AND
                Enrichment_Complete__c = False
        """

        accounts = []
        records = self.api.query(sql)['records']
        for record in records:
            account = {
                'sfid': record['Id'],
                'doid': record['DSCORGPKG__DiscoverOrg_ID__c'] or '',
                'prep': record['Enrichment_Requested_By__c'] or '0050V000006j7Jj',
                'name': record['Name'],
                'domain': record['Website'],
                'phone': record['Phone'],
                'status': 'enrich'}

            accounts.append(account)

        return accounts

    def get_contacts(self, account):
        """ Collects contacts for an account.

        :param account: an Account object
        :return contacts: a list of dictionaries of contact data
        """
        sql = """
            SELECT
                Id, Name, Title,
                Phone, MobilePhone, Email
            FROM
                Contact
            WHERE
                AccountId = '{sfid}'
        """.format(sfid=account.sfid)

        contacts = []
        records = self.api.query(sql)['records']
        for record in records:
            contact = {
                'account': account,
                'sfid': record['Id'],
                'name': record['Name'],
                'title': record['Title'],
                'office': account.phone,
                'direct': record['Phone'],
                'mobile': record['MobilePhone'],
                'email': record['Email'],
                'ctype': 'old',
                'status': 'upload'}

            contacts.append(contact)

        return contacts

    def create_contact(self, contact):
        """ Creates a new contact in Salesforce.

        :param contact: a Contact object
        """
        if contact.ctype != 'new':
            return

        for f in contact.account._meta.fields:
            if getattr(contact.account, f.name) is None:
                setattr(contact.account, f.name, '')

        for f in contact._meta.fields:
            if getattr(contact, f.name) is None:
                setattr(contact, f.name, '')

        name = contact.name.split()

        self.api.Contact.create({
            'AccountId': contact.account.sfid,
            'DSCORGPKG__DiscoverOrg_ID__c': contact.account.doid,
            'OwnerId': contact.account.prep,
            'FirstName': name[0],
            'LastName': name[1] if len(name) > 1 else name[0],
            'Title': contact.title,
            'Phone': contact.direct,
            'MobilePhone': contact.mobile,
            'Email': contact.email})

    def update_contact(self, contact):
        """ Updates a contact in Salesforce.
        :param contact: a Contact object
        """
        data = {
            'OwnerId': contact.account.prep,
            'Title': contact.title,
            'Phone': contact.direct or contact.account.phone,
            'MobilePhone': contact.mobile or ''}

        self.api.Contact.update(contact.sfid, data)


    def complete_account(self, account):
        """ Marks enrichment as complete.

        :param account: an Account object
        """
        data = {'Enrichment_Complete__c': True}

        try:
            self.api.Account.update(account.sfid, data)
        except:
            ErrorLog.objects.create(traceback=sys.exc_info())


class LushaClient:
    """ Implements a Lusha API client. """

    def __init__(self):
        self.token = os.environ['LUSHA_TOKEN']

    def enrich(self, contact):
        """ Enriches a contact object.

        :param contact: a Contact object
        """
        name = contact.name.split()
        if len(name) < 2:
            return
        elif len(name) == 3:
            name.pop(1)
        elif len(name) > 3:
            name = [name[0], name[1]]

        response = requests.get(
            'https://api.lusha.co/person',
            headers={
                'api_key': self.token},
            params={
                'firstName': name[0],
                'lastName': name[1],
                'company': contact.account.name,
                'property': 'phoneNumbers'})

        if 'errors' in response:
            return
        else:
            data = json.loads(response.text)

        numbers = data['phoneNumbers'] if 'phoneNumbers' in data else None
        emails = data['emailAddresses'] if 'emailAddresses' in data else None

        if numbers:
            contact.direct = numbers[0]['localizedNumber']
            if len(numbers) > 1:
                contact.mobile = numbers[1]['localizedNumber']
        else:
            return

        if emails:
            contact.email = emails[0]['email']

        contact.save()


class DiscoverOrgClient:
    """ Implements a DiscoverOrg API client. """

    def __init__(self):
        self.base = 'https://papi.discoverydb.com/papi'

        self.username = os.environ['DO_USERNAME']
        self.password = os.environ['DO_PASSWORD']
        self.key = os.environ['DO_KEY']

        self.session = self._get_session()

    def _get_session(self):
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
        session = response.headers['X-AUTH-TOKEN']

        return session

    def get_contacts(self, account):
        """ Searches for contacts under an account.

        :param account: an Account object
        :return contacts: a list of dictionaries of contact data
        """
        response = requests.post(
            url=''.join([self.base, '/v1/search/persons']),
            headers={
                'X-PARTNER-KEY': self.key,
                'X-AUTH-TOKEN': self.session,
                'Accept': 'application/json',
                'Content-Type': 'application/json'},
            data=json.dumps({
                'companyCriteria': {
                    'websiteUrls': [account.domain]}}))

        data = json.loads(response.text)

        contacts = []
        results = data['content']
        for result in results:
            contact = {
                'doid': result['id'],
                'name': result['fullName'],
                'title': (
                    result['title']
                    if 'title' in result
                    else None),
                'direct': (
                    result['officeTelNumber']
                    if 'officeTelNumber' in result
                    else account.phone),
                'mobile': (
                    result['mobileTelNumber']
                    if 'mobileTelNumber' in result
                    else None),
                'email': (
                    result['email']
                    if 'email' in result
                    else None),
                'ctype': 'new',
                'status': 'enrich'}

            contacts.append(contact)

        return contacts

    def get_hierarchy(self, account):
        """ Gets an org heirarchy graph for an account.

        :param account: an Account object
        :return hierarchy: a dictionary representing org hierarchy
        """
        if not account.doid:
            return {'message': 'Unavailable'}

        response = requests.get(
            url=''.join(
                [self.base, f"/v1/companies/{account.doid}/orgchart/7"]),
            headers={
                'X-PARTNER-KEY': self.key,
                'X-AUTH-TOKEN': self.session})

        data = json.loads(response.text)

        return data
