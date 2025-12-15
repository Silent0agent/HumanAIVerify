__all__ = ()

from io import BytesIO

from django import forms
from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

import tasks.forms
import tasks.models

User = auth.get_user_model()


class TestHelpers:
    class BaseTaskFormTest(TestCase):
        form_class = None
        payload_field_name = None

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            if cls.form_class:
                cls.model = cls.form_class.Meta.model

        def get_valid_data(self):
            return {
                self.model.title.field.name: "Test Task Title",
                self.model.description.field.name: "Test Description",
            }, {}

        def test_form_create_valid(self):
            data, files = self.get_valid_data()
            form = self.form_class(data=data, files=files)
            self.assertTrue(form.is_valid(), form.errors)

            self.assertEqual(
                form.cleaned_data[self.model.title.field.name],
                "Test Task Title",
            )

        def test_form_invalid_missing_payload(self):
            if not self.payload_field_name:
                return

            data, files = self.get_valid_data()

            if self.payload_field_name in data:
                del data[self.payload_field_name]

            if self.payload_field_name in files:
                del files[self.payload_field_name]

            form = self.form_class(data=data, files=files)
            self.assertFalse(form.is_valid())
            self.assertIn(self.payload_field_name, form.errors)

    class BaseCheckFormTest(TestCase):
        form_class = None

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            if cls.form_class:
                cls.model = cls.form_class.Meta.model
                cls.task_model = cls.model.task.field.related_model

            cls.customer = User.objects.create_user(
                username="client_base",
                email="client_base@t.com",
                password="pass",
            )
            cls.performer = User.objects.create_user(
                username="performer_base",
                email="performer_base@t.com",
                password="pass",
            )

        def create_task(self):
            raise NotImplementedError

        def get_valid_form_data(self):
            return {
                self.model.ai_score.field.name: 80.0,
                self.model.comment.field.name: "Valid comment",
            }

        def setUp(self):
            self.task = self.create_task()

        def test_widgets_attrs(self):
            form = self.form_class()
            ai_widget = form.fields[self.model.ai_score.field.name].widget
            self.assertEqual(ai_widget.attrs["min"], "0")
            self.assertEqual(ai_widget.attrs["max"], "100")
            self.assertEqual(ai_widget.attrs["step"], "0.1")

        def test_cannot_edit_published_check(self):
            check_kwargs = {
                self.model.task.field.name: self.task,
                self.model.performer.field.name: self.performer,
                self.model.ai_score.field.name: 50.0,
                self.model.comment.field.name: "Old comment",
                self.model.status.field.name: self.model.Status.PUBLISHED,
            }
            check = self.model.objects.create(**check_kwargs)

            data = self.get_valid_form_data()
            data[self.model.ai_score.field.name] = 99.9

            form = self.form_class(instance=check, data=data)

            self.assertFalse(form.is_valid())
            self.assertTrue(len(form.non_field_errors()) > 0)

        def test_can_edit_draft_check(self):
            check_kwargs = {
                self.model.task.field.name: self.task,
                self.model.performer.field.name: self.performer,
                self.model.ai_score.field.name: 50.0,
                self.model.status.field.name: self.model.Status.DRAFT,
            }
            check = self.model.objects.create(**check_kwargs)

            data = self.get_valid_form_data()
            data[self.model.ai_score.field.name] = 75.5

            form = self.form_class(instance=check, data=data)
            self.assertTrue(form.is_valid())

            updated_check = form.save()
            self.assertEqual(updated_check.ai_score, 75.5)


class TestTextTaskForm(TestHelpers.BaseTaskFormTest):
    form_class = tasks.forms.TextTaskForm
    payload_field_name = tasks.models.TextTask.content.field.name

    def get_valid_data(self):
        data, files = super().get_valid_data()
        data[self.payload_field_name] = "Some text content here"
        return data, files


class TestImageTaskForm(TestHelpers.BaseTaskFormTest):
    form_class = tasks.forms.ImageTaskForm
    payload_field_name = tasks.models.ImageTask.image.field.name

    def get_valid_data(self):
        data, files = super().get_valid_data()

        output = BytesIO()
        img = Image.new("RGB", (100, 100), color="white")
        img.save(output, format="JPEG")
        output.seek(0)

        image_file = SimpleUploadedFile(
            "test.jpg",
            output.read(),
            content_type="image/jpeg",
        )

        files[self.payload_field_name] = image_file
        return data, files

    def test_widget_accept_attr(self):
        form = self.form_class()
        widget = form.fields[self.payload_field_name].widget
        self.assertEqual(widget.attrs["accept"], "image/*")


class TestAudioTaskForm(TestHelpers.BaseTaskFormTest):
    form_class = tasks.forms.AudioTaskForm
    payload_field_name = tasks.models.AudioTask.audio.field.name

    def get_valid_data(self):
        data, files = super().get_valid_data()

        audio_file = SimpleUploadedFile(
            "test.mp3",
            b"fake_audio_bytes",
            content_type="audio/mpeg",
        )

        files[self.payload_field_name] = audio_file
        return data, files

    def test_widget_accept_attr(self):
        form = self.form_class()
        widget = form.fields[self.payload_field_name].widget
        self.assertEqual(widget.attrs["accept"], ".mp3, .wav")


class TestTextCheckForm(TestHelpers.BaseCheckFormTest):
    form_class = tasks.forms.TextTaskCheckForm

    def create_task(self):
        return self.task_model.objects.create(
            client=self.customer,
            title="Text Task",
            content="Some content",
        )

    def get_valid_form_data(self):
        data = super().get_valid_form_data()
        data["highlighted_content"] = (
            "<span class='haiv-highlight'>Some content</span>"
        )
        return data

    def test_hidden_field(self):
        form = self.form_class()
        self.assertIsInstance(
            form.fields["highlighted_content"].widget,
            forms.HiddenInput,
        )


class TestImageCheckForm(TestHelpers.BaseCheckFormTest):
    form_class = tasks.forms.ImageTaskCheckForm

    def create_task(self):
        image = SimpleUploadedFile("t.jpg", b"123", "image/jpeg")
        return self.task_model.objects.create(
            client=self.customer,
            title="Image Task",
            image=image,
        )


class TestAudioCheckForm(TestHelpers.BaseCheckFormTest):
    form_class = tasks.forms.AudioTaskCheckForm

    def create_task(self):
        audio = SimpleUploadedFile("t.mp3", b"123", "audio/mpeg")
        return self.task_model.objects.create(
            client=self.customer,
            title="Audio Task",
            audio=audio,
        )
