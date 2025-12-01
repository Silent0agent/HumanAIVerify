__all__ = ()

import http

import django.test
import django.urls


class StaticUrlsTests(django.test.TestCase):
    def test_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("about:about"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
