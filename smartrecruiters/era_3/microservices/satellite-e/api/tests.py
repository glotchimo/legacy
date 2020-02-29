"""
api.tests
~~~~~~~~~

This module implements the unit tests for the API.
"""

# pylint:disable=E1101

import os

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from api import views
from api.models import Account, Contact


TEST_TOKEN = os.getenv("SATELLITE_TOKEN")


class AccountTestCase(TestCase):
    def setUp(self):
        self.account0 = Account.objects.create(
            sfid="test0",
            prep="test0",
            status="test0",
            name="test0",
            domain="test0.com",
            phone="test0",
        )
        self.account1 = Account.objects.create(
            sfid="test1",
            prep="test1",
            status="test1",
            name="test1",
            domain="test1.com",
            phone="test1",
        )

    def test_get_accounts(self):
        factory = RequestFactory()
        request = factory.get("accounts", HTTP_AUTHORIZATION=TEST_TOKEN)

        response = views.get_accounts(request)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

        request = factory.get(
            "accounts", data={"name": "test0"}, HTTP_AUTHORIZATION=TEST_TOKEN
        )

        response = views.get_accounts(request)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertFalse(b"test1" in response.content)

    def test_create_account(self):
        factory = RequestFactory()
        request = factory.post(
            "accounts/create",
            data={
                "sfid": "test2",
                "prep": "test2",
                "status": "test2",
                "name": "test2",
                "domain": "test2.com",
                "phone": "test2",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=TEST_TOKEN,
        )

        response = views.create_account(request)
        self.assertEquals(response.status_code, 200)

    def test_update_account(self):
        factory = RequestFactory()
        request = factory.post(
            f"accounts/{self.account0.id}/update",
            data={"status": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION=TEST_TOKEN,
        )

        response = views.update_account(request, self.account0.id)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")

    def test_delete_account(self):
        account = Account.objects.create(
            sfid="test2",
            prep="test2",
            status="test2",
            name="test2",
            domain="test2.com",
            phone="test2",
        )

        factory = RequestFactory()
        request = factory.post(
            f"accounts/{account.id}/delete", HTTP_AUTHORIZATION=TEST_TOKEN
        )

        response = views.delete_account(request, account.id)
        self.assertEquals(response.status_code, 200)


class ContactTestCase(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            sfid="test3",
            prep="test3",
            status="test3",
            name="test3",
            domain="test3.com",
            phone="test3",
        )

        self.contact0 = Contact.objects.create(
            account=self.account, name="test0", title="test0"
        )
        self.contact1 = Contact.objects.create(
            account=self.account, name="test1", title="test1"
        )

    def test_get_contacts(self):
        factory = RequestFactory()
        request = factory.get("contacts", HTTP_AUTHORIZATION=TEST_TOKEN)

        response = views.get_contacts(request)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

        request = factory.get(
            "contacts", data={"name": "test0"}, HTTP_AUTHORIZATION=TEST_TOKEN
        )

        response = views.get_contacts(request)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertFalse(b"test1" in response.content)

    def test_create_contact(self):
        factory = RequestFactory()
        request = factory.post(
            "contacts/create",
            data={"name": "test0", "pid": self.account.id},
            content_type="application/json",
            HTTP_AUTHORIZATION=TEST_TOKEN,
        )

        response = views.create_contact(request)
        self.assertEquals(response.status_code, 200)

        request = factory.post(
            "contacts/create",
            data={"pid": self.account.id},
            content_type="application/json",
            HTTP_AUTHORIZATION=TEST_TOKEN,
        )

        response = views.create_contact(request)
        self.assertEquals(response.status_code, 200)

    def test_update_contact(self):
        factory = RequestFactory()
        request = factory.post(
            f"contacts/{self.contact0.id}",
            data={"title": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION=TEST_TOKEN,
        )

        response = views.update_contact(request, self.contact0.id)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")
