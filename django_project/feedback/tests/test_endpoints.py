__all__ = ()

import pathlib
import tempfile

import django.conf
import django.core.files
from django.test import Client, override_settings, TestCase
from django.urls import reverse

import feedback.forms
import feedback.models


class EndpointsTests(TestCase):
    def test_forms_in_context(self):
        response = Client().get(reverse("feedback:feedback"))

        forms = [
            "author_form",
            "content_form",
            "files_form",
        ]
        for form in forms:
            self.assertIn(form, response.context)

    def test_form_in_context_type(self):
        response = Client().get(reverse("feedback:feedback"))

        form_type_mapping = {
            "author_form": feedback.forms.FeedbackUserProfileForm,
            "content_form": feedback.forms.FeedbackForm,
            "files_form": feedback.forms.FeedbackFileForm,
        }

        for form, form_type in form_type_mapping.items():
            self.assertIsInstance(
                response.context[form],
                form_type,
            )

    def test_redirects(self):
        data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "test@email.com",
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_create_db_records(self):
        initial_amount_feedback = feedback.models.Feedback.objects.count()
        initial_amount_author = (
            feedback.models.FeedbackUserProfile.objects.count()
        )

        form_data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "test@email.com",
        }
        Client().post(reverse("feedback:feedback"), data=form_data)

        self.assertEqual(
            initial_amount_feedback + 1,
            feedback.models.Feedback.objects.count(),
        )
        self.assertEqual(
            initial_amount_author + 1,
            feedback.models.FeedbackUserProfile.objects.count(),
        )

    def test_form_invalid_data_not_create_db_records(self):
        initial_amount_feedback = feedback.models.Feedback.objects.count()
        initial_amount_author = (
            feedback.models.FeedbackUserProfile.objects.count()
        )

        form_data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "bad_email",
        }
        Client().post(reverse("feedback:feedback"), data=form_data)

        self.assertEqual(
            initial_amount_feedback,
            feedback.models.Feedback.objects.count(),
        )
        self.assertEqual(
            initial_amount_author,
            feedback.models.FeedbackUserProfile.objects.count(),
        )

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory().name)
    def test_files_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]
        form_data = {
            "name": "test_name",
            "text": "test_text_1",
            "mail": "test@mail.ru",
            "file": files,
        }
        django.test.Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        feedback_item = feedback.models.Feedback.objects.get(
            text="test_text_1",
        )
        self.assertEqual(feedback_item.files.count(), 10)

        media_root = pathlib.Path(django.conf.settings.MEDIA_ROOT)
        feedback_files = feedback_item.files.all()

        for index, file in enumerate(feedback_files):
            uploaded_file_path = media_root / file.file.path
            self.assertEqual(uploaded_file_path.open().read(), f"file_{index}")
