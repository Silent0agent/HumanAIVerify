__all__ = ()

from http import HTTPStatus

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

import homepage.views


class HomepageRoutesTest(SimpleTestCase):
    def test_index(self):
        url = reverse("homepage:index")
        self.assertEqual(url, "/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, homepage.views.IndexView)


class HomepageViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index_url = reverse("homepage:index")

    def test_index_status_code_ok(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_template(self):
        self.client.get(self.index_url)
        self.assertTemplateUsed("homepage/index.html")
