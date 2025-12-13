__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _
from multiupload.fields import MultiFileField

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
            feedback.models.Feedback.created_at.field.name,
        ]
        widgets = {
            feedback.models.Feedback.text.field.name: forms.Textarea(),
        }


class FeedbackFileForm(core.forms.BootstrapFormMixin, forms.Form):
    files = MultiFileField(
        min_num=0,
        max_num=10,
        max_file_size=16 * 1024 * 1024,
        label=_("upload_files"),
        help_text=_("upload_files_help_text"),
        required=False,
    )

    def save(self, feedback_instance):
        files = self.cleaned_data.get("files", [])
        created_files = []

        for each in files:
            instance = feedback.models.FeedbackFile.objects.create(
                feedback=feedback_instance,
                file=each,
            )
            created_files.append(instance)

        return created_files
