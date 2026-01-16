__all__ = ()

from django.test import TestCase

import training.forms
import training.models


class TrainingTextFormTest(TestCase):
    def test_form_has_field(self):
        form = training.forms.TrainingTextForm()
        self.assertIn(
            training.models.TrainingText.is_ai_generated.field.name,
            form.fields,
        )

    def test_form_valid_with_true(self):
        data = {training.models.TrainingText.is_ai_generated.field.name: True}
        form = training.forms.TrainingTextForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertTrue(
            form.cleaned_data[training.models.TrainingText.is_ai_generated.field.name],
        )

    def test_form_valid_with_false(self):
        data = {training.models.TrainingText.is_ai_generated.field.name: False}
        form = training.forms.TrainingTextForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertFalse(
            form.cleaned_data[training.models.TrainingText.is_ai_generated.field.name],
        )

    def test_form_invalid_with_empty(self):
        data = {}
        form = training.forms.TrainingTextForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            training.models.TrainingText.is_ai_generated.field.name,
            form.errors,
        )

    def test_init_pops_training_text(self):
        dummy_text = 'some text object'
        form = training.forms.TrainingTextForm(training_text=dummy_text)

        self.assertEqual(form.training_text, dummy_text)
