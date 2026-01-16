__all__ = ()

from pathlib import Path
import shutil
import tempfile

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

import feedback.forms
import feedback.models

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FeedbackIntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('feedback:feedback')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.valid_data = {
            'author-name': 'Test User',
            'author-mail': 'test@example.com',
            'content-text': 'This is a test feedback message.',
        }

    def test_feedback_page_status_code_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_feedback_page_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'feedback/feedback.html')

    def test_feedback_page_forms_in_context(self):
        response = self.client.get(self.url)

        expected_forms = {
            'author_form': feedback.forms.FeedbackUserProfileForm,
            'content_form': feedback.forms.FeedbackForm,
            'files_form': feedback.forms.FeedbackFileForm,
        }

        for form_key, form_class in expected_forms.items():
            with self.subTest(form=form_key):
                self.assertIn(form_key, response.context)
                self.assertIsInstance(response.context[form_key], form_class)

    def test_successful_submission_redirects_to_feedback(self):
        response = self.client.post(
            self.url,
            data=self.valid_data,
            follow=True,
        )

        self.assertRedirects(response, self.url)

    def test_successful_submission_creates_objects(self):
        initial_feedback_count = feedback.models.Feedback.objects.count()
        initial_profile_count = feedback.models.FeedbackUserProfile.objects.count()

        self.client.post(
            self.url,
            data=self.valid_data,
            follow=True,
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            initial_feedback_count + 1,
        )
        self.assertEqual(
            feedback.models.FeedbackUserProfile.objects.count(),
            initial_profile_count + 1,
        )

    def test_successful_submission_objects_data(self):
        self.client.post(
            self.url,
            data=self.valid_data,
            follow=True,
        )

        created_feedback = feedback.models.Feedback.objects.first()
        self.assertEqual(
            created_feedback.text,
            self.valid_data['content-text'],
        )
        self.assertEqual(
            created_feedback.author.name,
            self.valid_data['author-name'],
        )

    def test_successful_submission_sends_email(self):
        self.client.post(
            self.url,
            data=self.valid_data,
            follow=True,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.valid_data['author-mail']])

    def test_successful_submission_email_text(self):
        self.client.post(
            self.url,
            data=self.valid_data,
            follow=True,
        )

        self.assertIn(self.valid_data['content-text'], mail.outbox[0].body)

    def test_invalid_submission_status_code_ok(self):
        invalid_data = self.valid_data.copy()
        invalid_data['author-mail'] = 'not-an-email'
        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)

    def test_invalid_submission_does_not_create_objects(self):
        initial_feedback_count = feedback.models.Feedback.objects.count()

        invalid_data = self.valid_data.copy()
        invalid_data['author-mail'] = 'not-an-email'

        self.client.post(self.url, data=invalid_data)

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            initial_feedback_count,
        )

    def test_invalid_submission_form_errors(self):
        invalid_data = self.valid_data.copy()
        invalid_data['author-mail'] = 'not-an-email'

        response = self.client.post(self.url, data=invalid_data)

        author_form = response.context.get('author_form')
        self.assertTrue(author_form.errors)
        self.assertIn('mail', author_form.errors)

    def _post_feedback_with_files(self, count=1):
        files_to_upload = [
            SimpleUploadedFile(
                name=f'test_file_{i}.txt',
                content=f'content_{i}'.encode('utf-8'),
                content_type='text/plain',
            )
            for i in range(count)
        ]

        data = self.valid_data.copy()
        data['files-files'] = files_to_upload

        return self.client.post(self.url, data=data, follow=True)

    def test_upload_creates_db_records(self):
        expected_count = 2
        self._post_feedback_with_files(count=expected_count)
        feedback_obj = feedback.models.Feedback.objects.first()

        self.assertIsNotNone(feedback_obj)
        self.assertEqual(feedback_obj.files.count(), expected_count)

    def test_uploaded_file_path_structure(self):
        self._post_feedback_with_files(count=1)
        feedback_obj = feedback.models.Feedback.objects.first()
        saved_file = feedback_obj.files.first()

        self.assertTrue(
            saved_file.file.name.startswith('feedback/attachments/'),
        )
        self.assertTrue(saved_file.file.name.endswith('.txt'))

    def test_uploaded_file_content(self):
        self._post_feedback_with_files(count=1)

        feedback_obj = feedback.models.Feedback.objects.first()
        saved_file = feedback_obj.files.first()

        with Path(saved_file.file.path).open('rb') as f:
            content = f.read().decode('utf-8')

        self.assertEqual(content, 'content_0')
