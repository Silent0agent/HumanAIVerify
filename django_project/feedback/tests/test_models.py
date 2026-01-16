__all__ = ()

from django.test import TestCase
from parameterized import parameterized

import feedback.models


class FeedbackModelTests(TestCase):
    def test_feedback_default_status_is_received(self):
        feedback_item = feedback.models.Feedback.objects.create(
            text='Some text',
        )

        self.assertEqual(
            feedback_item.status,
            feedback.models.StatusChoices.RECEIVED,
        )

    def test_feedback_file_upload_path_logic(self):
        feedback_item = feedback.models.Feedback.objects.create(text='test')
        feedback_file = feedback.models.FeedbackFile(feedback=feedback_item)

        filename = 'my_image.jpg'
        generated_path = feedback_file.file_path(filename)
        expected_prefix = f'feedback/attachments/{feedback_item.id}/'

        self.assertTrue(generated_path.startswith(expected_prefix))
        self.assertTrue(generated_path.endswith('.jpg'))

        self.assertRegex(
            generated_path,
            r'feedback/attachments/\d+/[a-f0-9-]{36}\.jpg',
        )


class FeedbackStringRepresentationTests(TestCase):
    @parameterized.expand(
        [
            ('Short text', 'Short text'),
            ('123456789012', '123456789012'),
            (
                '1234567890123456789012345678901',
                '12345678901234567890123456789…',
            ),
            (
                'A very very very long text message',
                'A very very very long text me…',
            ),
        ],
    )
    def test_feedback_str_truncation(self, text, expected_str):
        feedback_item = feedback.models.Feedback(text=text)
        self.assertEqual(str(feedback_item), expected_str)

    def test_feedback_user_profile_str(self):
        profile = feedback.models.FeedbackUserProfile(
            mail='test@example.com',
            name='Test user',
        )
        self.assertEqual(str(profile), profile.mail)

    def test_status_log_str(self):
        feedback_item = feedback.models.Feedback.objects.create(
            text='Test text',
        )
        log = feedback.models.StatusLog(feedback=feedback_item)
        self.assertEqual(str(log), str(feedback_item))


class FeedbackRelationshipsTests(TestCase):
    def test_feedback_deletion_cascades_to_files(self):
        feedback_item = feedback.models.Feedback.objects.create(
            text='Some text',
        )
        feedback.models.FeedbackFile.objects.create(feedback=feedback_item)
        feedback.models.FeedbackFile.objects.create(feedback=feedback_item)

        self.assertEqual(feedback.models.FeedbackFile.objects.count(), 2)
        feedback_item.delete()
        self.assertEqual(feedback.models.FeedbackFile.objects.count(), 0)

    def test_author_deletion_does_not_delete_feedback(self):
        author = feedback.models.FeedbackUserProfile.objects.create(
            mail='author@test.com',
            name='Author',
        )
        feedback_item = feedback.models.Feedback.objects.create(
            text='Some text',
            author=author,
        )

        self.assertIsNotNone(feedback_item.author)
        author.delete()
        feedback_item.refresh_from_db()

        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                pk=feedback_item.pk,
            ).exists(),
        )
        self.assertIsNone(feedback_item.author)
