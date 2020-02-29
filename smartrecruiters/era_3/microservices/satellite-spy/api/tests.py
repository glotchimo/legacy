"""
api.tests
~~~~~~~~~

This module implements the unit tests for the API.
"""

# pylint:disable=E1101

import uuid

from api import views
from api.models import Competitor, Advantage, Objection, Resource, Insight, Comment

from django.core.files import temp
from django.test import TestCase
from django.test.client import RequestFactory


class CompetitorTestCase(TestCase):
    def setUp(self):
        self.test0uuid = uuid.uuid4()
        self.test1uuid = uuid.uuid4()
        Competitor.objects.create(
            id=self.test0uuid, name="test0", website="test.com", description="test0"
        )
        Competitor.objects.create(
            id=self.test1uuid, name="test1", website="test.com", description="test1"
        )

    def test_get_competitors(self):
        factory = RequestFactory()
        request = factory.get(
            "Competitor",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Competitor")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

        request = factory.get(
            "Competitor",
            data={"name": "test0"},
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Competitor")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertFalse(b"test1" in response.content)

    def test_update_competitor(self):
        factory = RequestFactory()
        request = factory.post(
            f"Competitor/{self.test0uuid}/update",
            data={"description": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.update(request, "Competitor", self.test0uuid)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")


class AdvantageTestCase(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            name="test0", website="test.com", description="test0"
        )

        self.test0uuid = uuid.uuid4()
        Advantage.objects.create(
            id=self.test0uuid, competitor=self.competitor, name="test0", script="test0"
        )
        self.test1uuid = uuid.uuid4()
        Advantage.objects.create(
            id=self.test1uuid, competitor=self.competitor, name="test1", script="test1"
        )

    def test_get_advantages(self):
        factory = RequestFactory()
        request = factory.get(
            "Advantage",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Advantage")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

    def test_create_advantage(self):
        factory = RequestFactory()

        request = factory.post(
            "Advantage/create",
            data={
                "name": "test2",
                "pid": str(self.competitor.id),
                "parent": "Competitor",
                "script": "test2",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.create(request, "Advantage")
        self.assertEquals(response.status_code, 200)

    def test_update_advantage(self):
        factory = RequestFactory()
        request = factory.post(
            f"Advantage/{self.test0uuid}/update",
            data={"name": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.update(request, "Advantage", self.test0uuid)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")

    def test_delete_advantage(self):
        factory = RequestFactory()
        request = factory.delete(
            f"Advantage/{self.test0uuid}/delete",
            HTTP_AUTHORIZATION="",
        )

        response = views.delete(request, "Advantage", self.test0uuid)
        self.assertEquals(response.status_code, 200)


class ObjectionTestCase(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            name="test0", website="test.com", description="test0"
        )

        self.test0uuid = uuid.uuid4()
        Objection.objects.create(
            id=self.test0uuid, competitor=self.competitor, name="test0", script="test0"
        )
        self.test1uuid = uuid.uuid4()
        Objection.objects.create(
            id=self.test1uuid, competitor=self.competitor, name="test1", script="test1"
        )

    def test_get_objections(self):
        factory = RequestFactory()
        request = factory.get(
            "Objection",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Objection")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

    def test_create_objection(self):
        factory = RequestFactory()

        request = factory.post(
            "Objection/create",
            data={
                "name": "test2",
                "pid": str(self.competitor.id),
                "parent": "Competitor",
                "script": "test2",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.create(request, "Objection")
        self.assertEquals(response.status_code, 200)

    def test_update_objection(self):
        factory = RequestFactory()
        request = factory.post(
            f"Objection/{self.test0uuid}/update",
            data={"name": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.update(request, "Objection", self.test0uuid)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")

    def test_delete_objection(self):
        factory = RequestFactory()
        request = factory.delete(
            f"Objection/{self.test0uuid}/delete",
            HTTP_AUTHORIZATION="",
        )

        response = views.delete(request, "Objection", self.test0uuid)
        self.assertEquals(response.status_code, 200)


class ResourceTestCase(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            name="test0", website="test.com", description="test0"
        )

        self.test0uuid = uuid.uuid4()
        Resource.objects.create(
            id=self.test0uuid,
            competitor=self.competitor,
            title="test0",
            link="https://httpbin.org/image",
            description="test0",
        )
        self.test1uuid = uuid.uuid4()
        Resource.objects.create(
            id=self.test1uuid,
            competitor=self.competitor,
            title="test1",
            link="https://httpbin.org/image",
            description="test1",
        )

    def test_get_resources(self):
        factory = RequestFactory()
        request = factory.get(
            "Resource",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Resource")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

    def test_create_resource(self):
        factory = RequestFactory()

        request = factory.post(
            "Resource/create",
            data={
                "pid": str(self.competitor.id),
                "parent": "Competitor",
                "title": "test2",
                "link": "https://httpbin.org/image",
                "description": "test2",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.create(request, "Resource")
        self.assertEquals(response.status_code, 200)

    def test_update_resource(self):
        factory = RequestFactory()
        request = factory.post(
            f"Resource/{self.test0uuid}/update",
            data={"title": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.update(request, "Resource", self.test0uuid)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")

    def test_delete_resource(self):
        factory = RequestFactory()
        request = factory.delete(
            f"Resource/{self.test0uuid}/delete",
            HTTP_AUTHORIZATION="",
        )

        response = views.delete(request, "Resource", self.test0uuid)
        self.assertEquals(response.status_code, 200)


class InsightTestCase(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            name="test0", website="test.com", description="test0"
        )

        self.test0uuid = uuid.uuid4()
        Insight.objects.create(
            id=self.test0uuid,
            competitor=self.competitor,
            title="test0",
            link="test.com",
            description="test0",
        )
        self.test1uuid = uuid.uuid4()
        Insight.objects.create(
            id=self.test1uuid,
            competitor=self.competitor,
            title="test1",
            link="test.com",
            description="test1",
        )

    def test_get_insights(self):
        factory = RequestFactory()
        request = factory.get(
            "insights",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Insight")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertContains(response, "test1")

        request = factory.get(
            "Insight",
            data={"title": "test0"},
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Insight")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0")
        self.assertFalse(b"test1" in response.content)

    def test_create_insight(self):
        factory = RequestFactory()
        request = factory.post(
            "Insight/create",
            data={
                "pid": str(self.competitor.id),
                "parent": "Competitor",
                "title": "test3",
                "link": "test.com",
                "description": "test3",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.create(request, "Insight")
        self.assertEquals(response.status_code, 200)

    def test_update_insight(self):
        factory = RequestFactory()
        request = factory.post(
            f"Insight/{self.test0uuid}/update",
            data={"description": "test0_new"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.update(request, "Insight", self.test0uuid)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test0_new")

    def test_delete_insight(self):
        factory = RequestFactory()
        request = factory.delete(
            f"Insight/{self.test0uuid}/delete",
            HTTP_AUTHORIZATION="",
        )

        response = views.delete(request, "Insight", self.test0uuid)
        self.assertEquals(response.status_code, 200)


class CommentTestCase(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            name="test0", website="test.com", description="test0"
        )
        self.insight = Insight.objects.create(
            competitor=self.competitor,
            title="test0",
            link="test.com",
            description="test0",
        )

        self.test0uuid = uuid.uuid4()
        Comment.objects.create(
            id=self.test0uuid, insight=self.insight, content="test0")
        self.test1uuid = uuid.uuid4()
        Comment.objects.create(
            id=self.test1uuid, insight=self.insight, content="test1")

    def test_get_comments(self):
        factory = RequestFactory()
        request = factory.get(
            "Comment",
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Comment")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.test0uuid)
        self.assertContains(response, self.test1uuid)

        request = factory.get(
            "Comment",
            data={"id": self.test0uuid},
            HTTP_AUTHORIZATION="",
        )

        response = views.get(request, "Comment")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.test0uuid)
        self.assertFalse(bytes(str(self.test1uuid), "utf-8")
                         in response.content)

    def test_create_comment(self):
        factory = RequestFactory()
        request = factory.post(
            "Comment/create",
            data={"pid": str(self.insight.id),
                  "parent": "Insight", "content": "test3"},
            content_type="application/json",
            HTTP_AUTHORIZATION="",
        )

        response = views.create(request, "Comment")
        self.assertEquals(response.status_code, 200)

    def test_delete_comment(self):
        factory = RequestFactory()
        request = factory.delete(
            f"Comment/{self.test0uuid}/delete",
            HTTP_AUTHORIZATION="",
        )

        response = views.delete(request, "Comment", self.test0uuid)
        self.assertEquals(response.status_code, 200)
