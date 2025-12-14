__all__ = ()

from datetime import timedelta

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase

import tasks.models

User = auth.get_user_model()


class TestHelpers:
    class BaseTaskModelTest(TestCase):
        model = None
        check_model = None

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.client_user = User.objects.create_user(
                username="customer",
                password="password",
                email="email1@test.com",
            )
            cls.performer_user = User.objects.create_user(
                username="performer",
                password="password",
                email="email2@test.com",
            )
            cls.task_title = "Test task"

        def get_task_data(self):
            raise NotImplementedError

        def setUp(self):
            task_kwargs = {
                self.model.client.field.name: self.client_user,
                self.model.title.field.name: self.task_title,
                **self.get_task_data(),
            }
            self.task = self.model.objects.create(**task_kwargs)

        def test_task_timestamps(self):
            self.assertIsNotNone(self.task.created_at)
            self.assertIsNotNone(self.task.updated_at)

        def test_task_str(self):
            self.assertEqual(str(self.task), self.task_title)

        def test_description_empty(self):
            self.assertEqual(self.task.description, "")

        def test_setting_description(self):
            description_example = "Some description"
            self.task.description = description_example
            self.task.save()
            self.assertEqual(self.task.description, description_example)

        def test_ai_score_none(self):
            self.assertAlmostEqual(self.task.ai_score, None)

        def test_ai_score_calculation(self):
            self.check_model.objects.create(
                task=self.task,
                performer=self.performer_user,
                ai_score=50.0,
                status=self.check_model.Status.PUBLISHED,
            )
            performer_2 = User.objects.create_user(
                username="performer_2",
                password="password",
                email="email3@test.com",
            )
            self.check_model.objects.create(
                task=self.task,
                performer=performer_2,
                ai_score=100.0,
                status=self.check_model.Status.PUBLISHED,
            )
            self.task.refresh_from_db()
            self.assertAlmostEqual(self.task.ai_score, 75.0)

        def test_ordering_by_created_at_field(self):
            task_2 = self.model.objects.create(
                client=self.client_user,
                title="Test title",
                created_at=self.task.created_at + timedelta(seconds=10),
            )
            tasks = self.model.objects.all()
            self.assertEqual(tasks[0], task_2)
            self.assertEqual(tasks[1], self.task)

        def test_on_delete_client_protect(self):
            new_client = User.objects.create_user(
                username="client_2",
                email="client_2@test.com",
            )

            task_kwargs = {
                self.model.client.field.name: new_client,
                self.model.title.field.name: "Task 2",
                **self.get_task_data(),
            }
            self.model.objects.create(**task_kwargs)

            with self.assertRaises(ProtectedError):
                new_client.delete()

    class BaseCheckModelTest(TestCase):
        model = None
        task_model = None

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.client_user = User.objects.create_user(
                username="customer",
                password="pass",
                email="customer@email.com",
            )
            cls.performer_user = User.objects.create_user(
                username="performer",
                password="pass",
                email="performer@email.com",
            )
            cls.check_ai_score = 85.5

        def get_task_data(self):
            raise NotImplementedError

        def setUp(self):
            self.task = self.task_model.objects.create(
                client=self.client_user,
                title="Task Title",
                **self.get_task_data(),
            )
            self.check = self.model.objects.create(
                task=self.task,
                performer=self.performer_user,
                ai_score=self.check_ai_score,
                comment="Comment",
            )

        def test_check_str(self):
            self.assertEqual(
                str(self.check),
                f"{self.task.title} | {self.performer_user.username} "
                f"({self.check_ai_score}%)",
            )

        def test_check_timestamps(self):
            self.assertIsNotNone(self.check.created_at)
            self.assertIsNotNone(self.check.updated_at)

        def test_check_default_status_draft(self):
            self.assertEqual(self.check.status, self.model.Status.DRAFT)

        def test_ai_score_validators_min(self):
            self.check.ai_score = -0.1
            with self.assertRaises(ValidationError):
                self.check.full_clean()

        def test_ai_score_validators_max(self):
            self.check.ai_score = 100.1
            with self.assertRaises(ValidationError):
                self.check.full_clean()

        def test_unique_constraint_task_and_performer(self):
            with self.assertRaises(IntegrityError):
                self.model.objects.create(
                    task=self.task,
                    performer=self.performer_user,
                    ai_score=10.0,
                )

        def test_invalid_status(self):
            self.check.status = "invalid_status"
            with self.assertRaises(ValidationError):
                self.check.full_clean()

        def test_ordering_by_created_at_field(self):
            performer_user_2 = User.objects.create_user(
                username="performer_2",
                password="password",
                email="example3@email.com",
            )
            check_2 = self.model.objects.create(
                task=self.task,
                performer=performer_user_2,
                ai_score=35.0,
                comment="Looks like human",
                created_at=self.check.created_at + timedelta(seconds=10),
            )
            checks = self.model.objects.all()
            self.assertEqual(checks[0], check_2)
            self.assertEqual(checks[1], self.check)

        def test_on_delete_task_cascade(self):
            task_2 = self.task_model.objects.create(
                client=self.client_user,
                title="Task 2",
            )
            self.model.objects.create(
                task=task_2,
                performer=self.performer_user,
                ai_score=35.0,
                comment="Looks like human",
            )
            self.assertEqual(self.model.objects.count(), 2)
            task_2.delete()
            self.assertEqual(self.model.objects.count(), 1)

        def test_on_delete_performer_protect(self):
            performer_user_2 = User.objects.create_user(
                username="performer_2",
                password="password",
                email="example3@email.com",
            )
            self.model.objects.create(
                task=self.task,
                performer=performer_user_2,
                ai_score=35.0,
                comment="Looks like human",
            )
            self.assertEqual(User.objects.count(), 3)
            with self.assertRaises(ProtectedError):
                performer_user_2.delete()

            self.assertEqual(User.objects.count(), 3)


class TextTaskModelTest(TestHelpers.BaseTaskModelTest):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck

    def get_task_data(self):
        return {self.model.content.field.name: "Some text content"}

    def test_ckeditor_field_save_and_retrieve(self):
        html_content = (
            "<p>This is some <strong>rich</strong> text content "
            "with a <a href='https://example.com'>link</a>.</p>"
        )

        task = self.model.objects.create(
            client=self.client_user,
            title="Test Article",
            content=html_content,
        )

        retrieved_task = self.model.objects.get(id=task.id)
        self.assertEqual(retrieved_task.content, html_content)
        self.assertIn("<strong>rich</strong>", retrieved_task.content)


class TextCheckModelTest(TestHelpers.BaseCheckModelTest):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask

    def get_task_data(self):
        return {self.task_model.content.field.name: "Some text content"}

    def test_annotated_content_stores_html_tags(self):
        annotated_html = (
            "Some <span class='highlight' style='color: red;'>"
            "text</span> content"
        )

        self.check.annotated_content = annotated_html
        self.check.save()
        self.check.refresh_from_db()

        self.assertEqual(self.check.annotated_content, annotated_html)
        self.assertIn("<span", self.check.annotated_content)
        self.assertIn("</span>", self.check.annotated_content)

    def test_annotated_content_contains_original_text(self):
        original_content = self.task.content

        annotated_version = self.task.content.replace(
            "text",
            "<span class='haiv-highlight'>text</span>",
        )

        self.check.annotated_content = annotated_version
        self.check.save()
        self.assertGreater(
            len(self.check.annotated_content),
            len(original_content),
        )

        self.assertIn("Some", self.check.annotated_content)
        self.assertIn("content", self.check.annotated_content)


class ImageTaskModelTest(TestHelpers.BaseTaskModelTest):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck

    def get_task_data(self):
        image = SimpleUploadedFile("t.jpg", b"123", "image/jpeg")
        return {self.model.image.field.name: image}


class ImageCheckModelTest(TestHelpers.BaseCheckModelTest):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask

    def get_task_data(self):
        image = SimpleUploadedFile("t.jpg", b"123", "image/jpeg")
        return {self.task_model.image.field.name: image}


class AudioTaskModelTest(TestHelpers.BaseTaskModelTest):
    model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck

    def get_task_data(self):
        audio = SimpleUploadedFile(
            name="test_audio.mp3",
            content=b"\x00\x01",
            content_type="audio/mpeg",
        )
        return {self.model.audio.field.name: audio}

    def test_file_extension_validation(self):
        image = SimpleUploadedFile("t.jpg", b"123", "image/jpeg")
        with self.assertRaises(ValidationError):
            task = self.model(
                client=self.client_user,
                title="Some title",
                audio=image,
            )
            task.full_clean()


class AudioCheckModelTest(TestHelpers.BaseCheckModelTest):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask

    def get_task_data(self):
        audio = SimpleUploadedFile(
            name="test_audio.mp3",
            content=b"\x00\x01",
            content_type="audio/mpeg",
        )
        return {self.task_model.audio.field.name: audio}
