__all__ = ()

from http import HTTPStatus

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

import about.views


class AboutRoutesTest(SimpleTestCase):
    def test_about(self):
        url = reverse("about:about")
        self.assertEqual(url, "/about/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, about.views.AboutView)


class AboutViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.about_url = reverse("about:about")

    def test_about_status_code_ok(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_template(self):
        self.client.get(self.about_url)
        self.assertTemplateUsed("about/about.html")
