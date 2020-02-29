"""
api.tests
~~~~~~~~~

This module implements the unit tests for the API.
"""

# pylint:disable=E1101

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from api import views
from api.models import Profile


class AuthTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            "test",
            email="test@test.test",
            password="test",
            first_name="test",
            last_name="test",
        )
        Profile.objects.create(
            user=user, cid="test", status="pending", sfid="test", token="test"
        )

    def test_authentication(self):
        factory = RequestFactory()
        request = factory.get(
            "authenticate", HTTP_X_USERNAME="test", HTTP_X_PASSWORD="test"
        )

        response = views.authenticate(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response["X-Token"], "test")

    def test_authorization(self):
        factory = RequestFactory()
        request = factory.get("authorize", HTTP_AUTHORIZATION="Basic test")

        response = views.authorize(request)
        self.assertEquals(response.status_code, 200)


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            "tester", email="tester@test.test", password="test"
        )
        Profile.objects.create(user=user, cid="test", sfid="test", token="test")

    def test_user_flow(self):
        factory = RequestFactory()
        request = factory.post(
            "create",
            data={
                "sfid": "test_sfid",
                "email": "test@smartrecruiters.com",
                "password": "test_password",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
            content_type="application/json",
        )

        response = views.create_user(request)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get_by_natural_key("test@smartrecruiters.com")
        profile = Profile.objects.get(user=user)

        factory = RequestFactory()
        request = factory.get(
            "confirm", data={"username": "test@smartrecruiters.com", "cid": profile.cid}
        )

        response = views.confirm_user(request)
        self.assertEquals(response.status_code, 302)

        user = User.objects.get_by_natural_key("test@smartrecruiters.com")
        profile = Profile.objects.get(user=user)
        self.assertEquals(profile.status, "confirmed")

    def test_get_users(self):
        factory = RequestFactory()
        request = factory.get(
            "get", HTTP_X_USERNAME="tester", HTTP_AUTHORIZATION="Basic test"
        )

        response = views.get_users(request)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"test", response.content)

        request = factory.post("get", HTTP_AUTHORIZATION="Basic test")

        response = views.get_users(request)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"test", response.content)
