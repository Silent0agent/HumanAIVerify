__all__ = ()

from django.test import TestCase

import feedback.forms


class FeedbackUserProfileFormTests(TestCase):
    def test_name_field_is_optional(self):
        form = feedback.forms.FeedbackUserProfileForm(
            data={"mail": "user@email.com"},
        )
        self.assertTrue(form.is_valid())

    def test_email_validation_logic(self):
        form = feedback.forms.FeedbackUserProfileForm(
            data={
                "name": "test_name",
                "mail": "not-an-email",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mail", form.errors)
