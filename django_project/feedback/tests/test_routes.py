__all__ = ()

from django.test import SimpleTestCase
from django.urls import resolve, reverse

import feedback.views


class AuthRoutesTest(SimpleTestCase):
    def test_feedback(self):
        url = reverse('feedback:feedback')
        self.assertEqual(url, '/feedback/')

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, feedback.views.FeedbackView)
