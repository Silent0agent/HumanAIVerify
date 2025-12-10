__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

import tasks.models

User = auth.get_user_model()


class TextTaskCreationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_create_url = reverse("tasks:text-task-create")

        cls.valid_task_data = {
            "title": "Title",
            "description": "My task",
            "content": "Text to check",
        }

        cls.customer = User.objects.create_user(
            username="test_customer",
            email="customer@email.com",
            password="S3cure_P@ssw0rd!",
            is_active=True,
            role=User.Role.CUSTOMER,
        )

    def setUp(self):
        self.client.force_login(self.customer)

    def test_get_status_code_ok(self):
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.task_create_url)
        self.assertTemplateUsed(response, "tasks/task_create.html")

    def test_post_valid_status_code_found(self):
        response = self.client.post(
            self.task_create_url,
            self.valid_task_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_valid_creates_text_task(self):
        initial_count = tasks.models.TextTask.objects.count()

        self.client.post(self.task_create_url, self.valid_task_data)

        self.assertEqual(
            tasks.models.TextTask.objects.count(),
            initial_count + 1,
        )

    def test_post_valid_created_text_task_fields(self):
        self.client.post(self.task_create_url, self.valid_task_data)

        task = tasks.models.TextTask.objects.filter(
            client=self.customer,
        ).last()

        self.assertIsNotNone(task)
        for field, expected_value in self.valid_task_data.items():
            with self.subTest(field=field):
                actual_value = getattr(task, field)
                self.assertEqual(
                    actual_value,
                    expected_value,
                )


class TextTaskCheckPerformTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.customer = User.objects.create_user(
            username="customer",
            email="c@email.com",
            password="pwd",
            role=User.Role.CUSTOMER,
        )

        cls.performer = User.objects.create_user(
            username="performer",
            email="p@email.com",
            password="pwd",
            is_active=True,
            role=User.Role.PERFORMER,
        )

        cls.text_task = tasks.models.TextTask.objects.create(
            client=cls.customer,
            title="Task to Check",
            content="Some content",
        )
        cls.valid_check_data = {
            "ai_score": 75.0,
            "comment": "My comment",
            "action": "publish",
        }

        cls.url = reverse(
            "tasks:text-check-perform",
            kwargs={"task_id": cls.text_task.id},
        )

    def setUp(self):
        self.client.force_login(self.performer)

    def test_get_status_code_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/text_check_perform.html")

    def test_post_valid_status_code_found(self):
        response = self.client.post(self.url, self.valid_check_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_valid_creates_check(self):
        initial_count = tasks.models.TextTaskCheck.objects.count()
        self.client.post(self.url, self.valid_check_data)

        self.assertEqual(
            tasks.models.TextTaskCheck.objects.count(),
            initial_count + 1,
        )

    def test_post_valid_saves_fields_correctly(self):
        self.client.post(self.url, self.valid_check_data)

        check = tasks.models.TextTaskCheck.objects.filter(
            task=self.text_task,
            performer=self.performer,
        ).first()

        self.assertIsNotNone(check)
        expectations = [
            ("ai_score", self.valid_check_data["ai_score"]),
            ("comment", self.valid_check_data["comment"]),
            ("status", tasks.models.TextTaskCheck.Status.PUBLISHED),
        ]

        for field_name, expected_value in expectations:
            with self.subTest(field=field_name):
                actual_value = getattr(check, field_name)
                self.assertEqual(actual_value, expected_value)

    def test_post_valid_sets_published_status(self):
        self.client.post(self.url, self.valid_check_data)

        check = tasks.models.TextTaskCheck.objects.filter(
            task=self.text_task,
            performer=self.performer,
        ).first()

        self.assertEqual(
            check.status,
            tasks.models.TextTaskCheck.Status.PUBLISHED,
        )
