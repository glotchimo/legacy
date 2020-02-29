"""
app.utils
~~~~~~~~~~~~~~~~

This module implements all utilities for Pathfindr.

:copyright: (c) 2018 by Elliott Maguire
"""

import os
import time
import json

from app.models import Account, Contact

import requests
from ergal.profile import Profile
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceError


class SalesforceClient:
    def __init__(self):
        """ Initialize Salesforce API client.

        Credentials are sourced from environment variables,
        connection is created at initialization.
        
        """
        self.api = Salesforce(
            username=os.environ['SF_USERNAME'],
            password=os.environ['SF_PASSWORD'],
            security_token=os.environ['SF_TOKEN'],
            organizationId=os.environ['SF_ORG_ID'])

    def get_accounts(self):
        """ Collect accounts/tasks from Salesforce.

        Pulls accounts wherein enrichment or cleaning request
        is True, returns them as model-friendly dictionaries
        to be passed into Account models.

        Returns:
            list:accounts -- a list of account dicts
        
        """
        enrichments = self.api.query("""
            SELECT
                Id, Name, Phone, Website
            FROM
                Account
            WHERE
                Enrichment_Requested__c = True
            AND
                Enrichment_Complete__c = False
        """)

        accounts = []
        for record in enrichments['records']:
            account = {}
            account['sfid'] = record['Id']
            account['name'] = record['OB_Company_Name_Normalized__c']
            account['domain'] = record['Website']
            account['phone'] = record['Phone']
            account['status'] = 'enrich'
            accounts.append(account)
    
        return accounts
    
    def get_contacts(self, account):
        """ Collect contacts for accounts.
        
        Pulls in all existing contacts for the given account,
        returns them in a list of model-friendly dictionaries.

        Arguments:
            app.Account:account
        
        Returns:
            list:contacts -- a list of contact dicts
        
        """
        data = self.api.query(("""
            SELECT
                Id, Name, Title,
                Phone, MobilePhone, Email
            FROM
                Contact
            WHERE
                AccountId = '{sfid}'
        """).format(
            sfid=account.sfid))

        contacts = []

        for record in data['records']:
            contact = {}
            contact['account'] = account
            contact['sfid'] = record['Id']
            contact['name'] = record['Name']
            contact['title'] = record['Title']
            contact['office'] = account.phone
            contact['direct'] = record['Phone']
            contact['mobile'] = record['MobilePhone']
            contact['email'] = record['Email']
            contact['rating'] = None

            contacts.append(contact)
        
        return contacts

    def create_contact(self, account, contact):
        """ Create a new contact in Salesforce.

        Uses an enriched Contact object, creates a new contact
        record in Salesforce with the attached data.

        Arguments:
            app.Account:account -- an Account object
            app.Contact:contact -- a Contact object
        
        """
        for f in account._meta.fields:
            name = f.name
            value = getattr(account, name)
            if value is None:
                setattr(account, name, '')

        for f in contact._meta.fields:
            name = f.name
            value = getattr(contact, name)
            if value is None:
                setattr(contact, name, '')

        self.api.Contact.create({
                'AccountId': account.sfid,
                'FirstName': contact.name.split()[0],
                'LastName': contact.name.split()[1],
                'Title': contact.title,
                'Phone': contact.direct,
                'MobilePhone': contact.mobile,
                'Email': contact.email})
    
    def complete_account(self, account):
        """ Complete account in Salesforce.

        Marks the corresponding account in Salesforce
        as complete based on the request type.

        Arguments:
            app.Account:account -- an account object
        
        """
        self.api.Account.update(account.sfid, {
            'Enrichment_Complete__c': True,
            'Contact_Cleaning_Complete__c': True}
        )


class LushaClient:
    def __init__(self):
        """ Initialize Lusha API client.
        
        Though it uses ERGAL for most request processing,
        this class has blocks to parse out the desired data from
        returned records.

        This initialization assumes that the API profile for Lusha
        has already been created and is stored in a local ergal.db
        sqlite database file.

        """
        self.profile = Profile('Lusha API',
            base='https://api.lusha.co')
        
    def enrich(self, contact):
        """ Enrich a contact record.

        Using the properties of a contact object, a search
        is made in Lusha for direct, mobile, and email. If any
        data is added, the contact is updated.

        Arguments:
            app.Contact:contact -- a contact object.

        """
        name = contact.name.split()
        if len(name) > 2:
            name.pop(1)

        response = self.profile.call('Enrich Person', 
            params={
                'firstName': name[0],
                'lastName': name[1],
                'company': contact.account.name,
                'property': 'phoneNumbers'})

        if 'errors' in response:
            return
        
        Record.objects.create(
            source='Lusha',
            content=response,
            context='LushaClient: enrich')
        
        if 'phoneNumbers' in response['data']:
            numbers = response['data']['phoneNumbers']
        else:
            return
        
        if not 'emailAddresses' in response['data']:
            emails = response['data']['emailAddresses']
        else:
            emails = None

        if not contact.direct:
            contact.direct = numbers[0]['localizedNumber']
        
        if not contact.mobile:
            if len(numbers) > 1:
                contact.mobile = numbers[1]['localizedNumber']
        
        if emails:
            contact.email = emails[0]['email']
        
        contact.save()
    

class DiscoverOrgClient:
    def __init__(self):
        """ Initialize the DiscoverOrg API client.

        Also integrates pretty directly with ERGAL, but has some
        utility code to parse responses of different types.
        
        """
        self.profile = Profile('DiscoverOrg API',
            base='https://papi.discoverydb.com/papi/v1')
        
        session_key = self._get_session_key()
        self.profile.set_auth('key-header', 
            key=session_key,
            name='X-AUTH-TOKEN')
    
    def _get_session_key(self):
        """ Get a session key. """
        auth_url = 'https://papi.discoverydb.com/papi/login'
        auth_data = {
            'username': os.environ['DO_USERNAME'],
            'password': os.environ['DO_PASSWORD'],
            'partnerKey': os.environ['DO_KEY']}

        response = requests.post(auth_url, data=json.dumps(auth_data))
        session_key = response.headers['X-AUTH-TOKEN']

        return session_key
    
    def search(self, account):
        """ Search for contacts.

        Using the properties of an account object, a search
        is made in DiscoverOrg for all contacts under the
        given account. All of these records are returned in
        a list of model-friendly dictionaries.

        Arguments:
            app.Account:account -- an account object.
        
        Returns:
            list:contacts -- a list of contact dicts.
        
        """
        response = self.profile.call('Person Search',
            headers={
                'X-AUTH-TOKEN': str(self._get_session_key()),
                'Accept': 'application/json',
                'Content-Type': 'application/json'},
            data=json.dumps({
                'companyCriteria': {
                    'websiteUrls': [account.domain]}}))

        if len(response['content']) > 0:
            results = response['content']
        else:
            return
        
        classes = ['A', 'B', 'C']
        titles = [[
            'SENIOR VICE PRESIDENT', 'SVP', 'VICE PRESIDENT', 'VP',
            'PRESIDENT', 'CHIEF', 'DIRECTOR', 'HEAD', 'LEAD'], [
            'SENIOR MANAGER', 'MANAGER',
            'COORDINATOR', 'BUSINESS PARTNER'], [
            'ANALYST', 'GENERALIST', 'RECRUITER',
            'ASSISTANT', 'SPECIALIST']]
        
        contacts = []
        for result in results:
            contact = {}

            contact['category'] = 'enrich'
            contact['status'] = 'enrich'
            contact['dorgid'] = result['id']
            contact['name'] = result['fullName']
            if 'officeTelNumber' in result:
                contact['direct'] = result['officeTelNumber']
            if 'mobileTelNumber' in result:
                contact['mobile'] = result['mobileTelNumber']
            if 'email' in result:
                contact['email'] = result['email']
            
            if 'title' in result:
                contact['title'] = result['title']
            else:
                contact['title'] = 'Unknown'
            
            for sect in titles:
                for title in sect:
                    if title in contact['title'].upper():
                        contact['rating'] = classes[titles.index(sect)]
                        break
                    else:
                        continue

            if not 'rating' in contact:
                contact['rating'] = 'C'
            
            contact['status'] = 'enrich'

            contacts.append(contact)
        
        return contacts

