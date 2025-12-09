__all__ = ()

from django.test import SimpleTestCase
from django.urls import resolve, reverse

import tasks.views


class TasksRoutesTest(SimpleTestCase):
    def test_create(self):
        url = reverse("tasks:text-task-create")
        self.assertEqual(url, "/tasks/text-task/create/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            tasks.views.TextTaskCreateView,
        )

    def test_check(self):
        url = reverse("tasks:text-check-perform", kwargs={"task_id": 1})
        self.assertEqual(url, "/tasks/text-task/1/check/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            tasks.views.TextTaskCheckPerformView,
        )
