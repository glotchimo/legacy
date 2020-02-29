"""
api.clients
~~~~~~~~~~~

This module implements the client classes for the API.
"""

import os
import re
import sys
import json

from api.models import ErrorLog

import requests
import simple_salesforce


class SalesforceClient:
    """ Client for the Salesforce API. """

    def __init__(self):
        self.api = simple_salesforce.Salesforce(
            username=os.getenv("SF_USERNAME"),
            password=os.getenv("SF_PASSWORD"),
            security_token=os.getenv("SF_TOKEN"),
            organizationId=os.getenv("SF_ORG_ID"),
        )

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
        records = self.api.bulk.Account.query(sql)
        for record in records:
            account = {
                "sfid": record.get("Id", ""),
                "doid": record.get("DSCORGPKG__DiscoverOrg_ID__c", ""),
                "prep": record.get("Enrichment_Requested_By__c", "0050V000006j7Jj"),
                "name": record.get("Name", ""),
                "domain": record.get("Website", ""),
                "phone": record.get("Phone", ""),
                "status": "enrich",
            }

            accounts.append(account)

        return accounts

    def get_delta_accounts(self):
        """ Collects delta accounts from Salesforce.

        :return accounts: a list of dictionaries of account data
        """
        sql = """
            SELECT
                Id, OwnerId, DSCORGPKG__DiscoverOrg_ID__c, Name, Phone, Website
            FROM
                Account
            WHERE
                Id not in (select AccountId from Contact)
            AND
                Market_Segment__c = 'Commercial ENT'
            AND
                OB_Tier__c = 'Tier 1'

            LIMIT 100
        """

        accounts = []
        records = self.api.bulk.Account.query(sql)
        for record in records:
            account = {
                "sfid": record.get("Id", ""),
                "doid": record.get("DSCORGPKG__DiscoverOrg_ID__c", ""),
                "prep": record.get("OwnerId", "0050V000006j7Jj"),
                "name": record.get("Name", ""),
                "domain": record.get("Website", ""),
                "phone": record.get("Phone", ""),
                "status": "delta-new",
            }

            accounts.append(account)

        return accounts

    def get_contacts(self, account):
        """ Collects contacts for an account.

        :param account: an Account object.
        :return contacts: a list of dictionaries of contact data.
        """
        sql = f"""
            SELECT
                Id, Name, Title,
                Phone, MobilePhone, Email,
                Contact_Status__c
            FROM
                Contact
            WHERE
                AccountId = '{account.sfid}'
        """

        contacts = []
        records = self.api.bulk.Contact.query(sql)
        for record in records:
            contact = {
                "account": account,
                "sfid": record.get("Id", ""),
                "name": record.get("Name", ""),
                "title": record.get("Title", ""),
                "office": account.phone,
                "direct": record.get("Phone", ""),
                "mobile": record.get("MobilePhone", ""),
                "email": record.get("Email", ""),
                "ctype": "old",
                "status": "upload",
                "sf_status": record.get("Contact_Status__c", "New"),
            }

            contacts.append(contact)

        return contacts or []

    def create_contacts(self, contacts):
        """ Creates new contacts in Salesforce.

        :param contacts: a list of Contact objects.
        """
        load = []
        for contact in contacts:
            if contact.ctype != "new":
                return

            for f in contact.account._meta.fields:
                if getattr(contact.account, f.name) is None:
                    setattr(contact.account, f.name, "")

            for f in contact._meta.fields:
                if getattr(contact, f.name) is None:
                    setattr(contact, f.name, "")

            name = contact.name.split()

            record = {
                "AccountId": contact.account.sfid,
                "OwnerId": contact.account.prep,
                "FirstName": name[0],
                "LastName": name[1] if len(name) > 1 else "",
                "Title": contact.title,
                "Phone": contact.direct,
                "MobilePhone": contact.mobile,
                "Email": contact.email,
            }
            load.append(record)

        try:
            if load:
                self.api.bulk.Contact.insert(load)
        except:
            ErrorLog.objects.create(traceback=sys.exc_info())

            for contact in contacts:
                contact.status = "hold"
                contact.save()
        else:
            contacts.delete()

    def update_contacts(self, contacts):
        """ Updates contacts in Salesforce.

        :param contacts: a list of Contact objects.
        """
        for contact in contacts:
            record_initial = {
                "Id": contact.sfid,
                "AccountId": contact.account.sfid,
                "OwnerId": contact.account.prep,
                "Title": contact.title,
                "Email": contact.email,
                "Phone": contact.direct or contact.account.phone,
                "MobilePhone": contact.mobile or "",
                "Contact_Status__c": contact.sf_status,
            }
            record_final = record_initial.copy()

            for k, v in record_initial.items():
                if v is None or v == "":
                    record_final[k] = ""

            try:
                if record_final:
                    self.api.Contact.update(record_final)
            except:
                ErrorLog.objects.create(traceback=sys.exc_info())

                contact.status = "hold"
                contact.save()
            else:
                contact.delete()

    def complete_accounts(self, accounts):
        """ Marks enrichment as complete on a list of accounts.

        :param accounts: a list of Account objects.
        """
        for account in accounts:
            record_initial = {"Id": account.sfid, "Enrichment_Complete__c": True}
            record_final = record_initial.copy()

            for k, v in record_initial.items():
                if v is None or v == "":
                    record_final[k] = ""

            try:
                if record_final:
                    self.api.Account.update(record_final)
            except:
                ErrorLog.objects.create(traceback=sys.exc_info())

                account.status = "hold"
                account.save()
            else:
                account.delete()


class DiscoverOrgClient:
    """ Implements a DiscoverOrg API client. """

    def __init__(self):
        self.base = "https://papi.discoverydb.com/papi"

        self.username = os.getenv("DO_USERNAME")
        self.password = os.getenv("DO_PASSWORD")
        self.key = os.getenv("DO_KEY")

        self.session = self._get_session()

    def _get_session(self):
        """ Gets a session key.

        :return session: a session key
        """
        url = "".join([self.base, "/login"])
        headers = {"Content-Type": "application/json"}
        data = {
            "username": self.username,
            "password": self.password,
            "partnerKey": self.key,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        session = response.headers.get("X-AUTH-TOKEN")

        return session

    def get_contacts(self, account):
        """ Searches for contacts under an account.

        :param account: an Account object
        :return contacts: a list of dictionaries of contact data
        """
        response = requests.post(
            url="".join([self.base, "/v1/search/persons"]),
            headers={
                "X-PARTNER-KEY": self.key,
                "X-AUTH-TOKEN": self.session,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps({"companyCriteria": {"websiteUrls": [account.domain]}}),
        )

        data = json.loads(response.text)

        contacts = []
        results = data["content"]
        for result in results:
            contact = {
                "doid": result.get("id"),
                "name": result.get("fullName"),
                "title": result.get("title"),
                "direct": result.get("officeTelNumber"),
                "mobile": result.get("mobileTelNumber"),
                "email": result.get("email"),
                "ctype": "new",
                "status": "enrich",
            }

            if (
                contact.get("email", "") != ""
                and type(contact.get("email")) is str
                and re.findall("@(\w.+)", contact.get("email"))[0]
                in re.findall(
                    "^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)",
                    account.domain,
                )
            ):
                contacts.append(contact)

        return contacts or []

    def get_hierarchy(self, account):
        """ Gets an org heirarchy graph for an account.

        :param account: an Account object
        :return hierarchy: a dictionary representing org hierarchy
        """
        if not account.doid:
            return {"message": "Unavailable"}

        response = requests.get(
            url="".join([self.base, f"/v1/companies/{account.doid}/orgchart/7"]),
            headers={"X-PARTNER-KEY": self.key, "X-AUTH-TOKEN": self.session},
        )

        data = json.loads(response.text)

        return data
