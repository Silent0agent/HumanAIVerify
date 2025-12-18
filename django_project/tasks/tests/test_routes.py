__all__ = ()

from django.test import SimpleTestCase
from django.urls import resolve, reverse

import tasks.views


class TestHelpers:
    class BaseTaskRoutesTest(SimpleTestCase):
        task_type = None
        view_my_tasks = None
        view_task_create = None
        view_task_detail = None
        view_my_checks = None
        view_check_perform = None
        view_check_detail = None

        def test_my_tasks(self):
            url_name = f"tasks:my-{self.task_type}-tasks"
            url = reverse(url_name)
            self.assertEqual(url, f"/tasks/{self.task_type}/my/")

            resolver = resolve(url)
            self.assertEqual(resolver.func.view_class, self.view_my_tasks)

        def test_task_create(self):
            url_name = f"tasks:{self.task_type}-task-create"
            url = reverse(url_name)
            self.assertEqual(url, f"/tasks/{self.task_type}/create/")

            resolver = resolve(url)
            self.assertEqual(resolver.func.view_class, self.view_task_create)

        def test_task_detail(self):
            url_name = f"tasks:{self.task_type}-task-detail"
            url = reverse(url_name, kwargs={"task_id": 1})
            self.assertEqual(url, f"/tasks/{self.task_type}/1/")

            resolver = resolve(url)
            self.assertEqual(resolver.func.view_class, self.view_task_detail)

        def test_my_checks(self):
            url = reverse(f"tasks:my-{self.task_type}-checks")
            self.assertEqual(url, f"/tasks/{self.task_type}/my-checks/")

            resolver = resolve(url)
            self.assertEqual(
                resolver.func.view_class,
                self.view_my_checks,
            )

        def test_check_perform(self):
            url = reverse(
                f"tasks:{self.task_type}-check-perform",
                kwargs={"task_id": 1},
            )
            self.assertEqual(url, f"/tasks/{self.task_type}/1/check/")

            resolver = resolve(url)
            self.assertEqual(
                resolver.func.view_class,
                self.view_check_perform,
            )

        def test_check_detail(self):
            url = reverse(
                f"tasks:{self.task_type}-check-detail",
                kwargs={"check_id": 1},
            )
            self.assertEqual(url, f"/tasks/{self.task_type}/check/1/")

            resolver = resolve(url)
            self.assertEqual(
                resolver.func.view_class,
                self.view_check_detail,
            )


class TextRoutesTest(TestHelpers.BaseTaskRoutesTest):
    task_type = "text"

    view_my_tasks = tasks.views.MyTextTasksListView
    view_task_create = tasks.views.TextTaskCreateView
    view_task_detail = tasks.views.TextTaskDetailView
    view_my_checks = tasks.views.MyTextChecksListView
    view_check_perform = tasks.views.TextTaskCheckPerformView
    view_check_detail = tasks.views.TextTaskCheckDetailView


class ImageRoutesTest(TestHelpers.BaseTaskRoutesTest):
    task_type = "image"

    view_my_tasks = tasks.views.MyImageTasksListView
    view_task_create = tasks.views.ImageTaskCreateView
    view_task_detail = tasks.views.ImageTaskDetailView
    view_my_checks = tasks.views.MyImageChecksListView
    view_check_perform = tasks.views.ImageTaskCheckPerformView
    view_check_detail = tasks.views.ImageTaskCheckDetailView


class AudioRoutesTest(TestHelpers.BaseTaskRoutesTest):
    task_type = "audio"

    view_my_tasks = tasks.views.MyAudioTasksListView
    view_task_create = tasks.views.AudioTaskCreateView
    view_task_detail = tasks.views.AudioTaskDetailView
    view_my_checks = tasks.views.MyAudioChecksListView
    view_check_perform = tasks.views.AudioTaskCheckPerformView
    view_check_detail = tasks.views.AudioTaskCheckDetailView
