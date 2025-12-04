__all__ = ()

from django.test import TestCase
from parameterized import parameterized

import feedback.forms


class FeedbackUserProfileFormErrorsTests(TestCase):
    def test_form_name_is_not_requered(self):
        form = feedback.forms.FeedbackUserProfileForm(
            {
                "mail": "test@email.com",
            },
        )
        self.assertFormError(form, "name", [])

    def test_form_validate_email(self):
        form = feedback.forms.FeedbackUserProfileForm(
            {
                "name": "test_name",
                "mail": "bad_email",
            },
        )
        self.assertFormError(
            form,
            "mail",
            "Enter a valid email address.",
        )


class FeedbackFormsTests(TestCase):
    @parameterized.expand(
        [
            (
                feedback.forms.FeedbackForm(),
                [
                    ("text", "feedback_text"),
                ],
            ),
            (
                feedback.forms.FeedbackUserProfileForm(),
                [
                    ("name", "Name"),
                    ("mail", "Email"),
                ],
            ),
            (
                feedback.forms.FeedbackFileForm(),
                [
                    ("file", "upload_files"),
                ],
            ),
        ],
    )
    def test_field_label(self, form, fields):
        for field, expected_label in fields:
            with self.subTest(form=form, field=field):
                field_label = form.fields[field].label
                self.assertEqual(field_label, expected_label)

    @parameterized.expand(
        [
            (
                feedback.forms.FeedbackForm(),
                [
                    ("text", "enter_feedback_text"),
                ],
            ),
            (
                feedback.forms.FeedbackUserProfileForm(),
                [
                    ("name", "enter_name"),
                    ("mail", "enter_email"),
                ],
            ),
            (
                feedback.forms.FeedbackFileForm(),
                [("file", "upload_files_help_text")],
            ),
        ],
    )
    def test_field_help_text(self, form, fields):
        for field, expected_help_text in fields:
            with self.subTest(form=form, field=field):
                field_help_text = form.fields[field].help_text
                self.assertEqual(field_help_text, expected_help_text)
