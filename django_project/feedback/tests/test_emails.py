__all__ = ()

from django.core import mail
from django.test import TestCase
from django.urls import reverse


class FeedbackEmailTests(TestCase):
    def test_feedback_sends_email(self):
        self.client.post(
            reverse("feedback:feedback"),
            data={
                "name": "test",
                "mail": "correct@email.com",
                "text": "test_text",
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("test_text", mail.outbox[0].body)
