__all__ = ()

from django.test import SimpleTestCase
from django.urls import resolve, reverse

import tasks.views


class AuthRoutesTest(SimpleTestCase):
    def test_create(self):
        url = reverse("tasks:create")
        self.assertEqual(url, "/tasks/create/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            tasks.views.TextTaskCreateView,
        )

    def test_check(self):
        url = reverse("tasks:check", kwargs={"task_id": 1})
        self.assertEqual(url, "/tasks/1/check/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            tasks.views.TaskCheckPerformView,
        )
