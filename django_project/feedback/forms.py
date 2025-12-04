__all__ = ()

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import core.forms
import feedback.models


class FeedbackUserProfileForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        feedback_user_profile_name_field = (
            feedback.models.FeedbackUserProfile.name.field.name
        )
        feedback_user_profile_mail_field = (
            feedback.models.FeedbackUserProfile.mail.field.name
        )
        model = feedback.models.FeedbackUserProfile
        fields = (
            feedback_user_profile_name_field,
            feedback_user_profile_mail_field,
        )
        labels = {
            feedback_user_profile_name_field: _("Name"),
            feedback_user_profile_mail_field: _("Email"),
        }
        help_texts = {
            feedback_user_profile_name_field: _(
                "enter_name",
            ),
            feedback_user_profile_mail_field: _(
                "enter_email",
            ),
        }
        widgets = {
            feedback_user_profile_name_field: forms.TextInput(),
            feedback_user_profile_mail_field: forms.EmailInput(),
        }


class FeedbackForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback
        fields = (feedback.models.Feedback.text.field.name,)
        labels = {
            feedback.models.Feedback.text.field.name: _("feedback_text"),
        }
        help_texts = {
            feedback.models.Feedback.text.field.name: _(
                "enter_feedback_text",
            ),
        }
        exclude = [
            feedback.models.Feedback.created_on.field.name,
        ]
        widgets = {
            feedback.models.Feedback.text.field.name: forms.Textarea(),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [forms.FileField.clean(self, d, initial) for d in data]

        return [forms.FileField.clean(self, data, initial)]


class FeedbackFileForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    MAX_FILE_SIZE = 16 * 1024 * 1024
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE // (1024 * 1024)

    file = MultipleFileField(
        required=False,
        label=_("upload_files"),
        help_text=_("upload_files_help_text"),
    )

    class Meta:
        model = feedback.models.FeedbackFile
        fields = ("file",)
        widgets = {
            "file": MultipleFileInput(
                attrs={
                    "type": "file",
                    "multiple": True,
                },
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        files = cleaned_data.get("file", [])

        if files:
            errors = []
            valid_files = []

            for uploaded_file in files:
                if uploaded_file.size > self.MAX_FILE_SIZE:
                    errors.append(
                        ValidationError(
                            _(
                                "file_max_size_error",
                            )
                            % {
                                "filename": uploaded_file.name,
                                "max_size": self.MAX_FILE_SIZE_MB,
                            },
                        ),
                    )
                else:
                    valid_files.append(uploaded_file)

            if errors:
                raise ValidationError({"file": errors})

            cleaned_data["file"] = valid_files

        return cleaned_data

    def save(self, commit=True, feedback_instance=None):
        if not feedback_instance:
            return []

        files = self.cleaned_data.get("file", [])
        created_files = []

        for uploaded_file in files:
            feedback_file = feedback.models.FeedbackFile(
                feedback=feedback_instance,
                file=uploaded_file,
            )
            if commit:
                feedback_file.save()

            created_files.append(feedback_file)

        return created_files
