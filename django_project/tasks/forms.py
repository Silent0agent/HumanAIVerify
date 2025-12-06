__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.models import TaskCheck, TextTask


class TextTaskForm(forms.ModelForm):
    class Meta:
        model = TextTask
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter_task_title"),
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": _("Paste_text_for_AI_detection"),
                },
            ),
        }

        labels = {
            "title": _("Title"),
            "content": _("Content"),
        }


class TaskCheckForm(forms.ModelForm):
    class Meta:
        model = TaskCheck
        fields = ["ai_score", "comment"]

        widgets = {
            "ai_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "placeholder": _("0-100_percent"),
                },
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Your_comments_optional"),
                },
            ),
        }

        labels = {
            "ai_score": _("AI_Probability_percent"),
            "comment": _("Comments"),
        }

        help_texts = {
            "ai_score": _("Enter_percentage_from_0_to_100"),
        }

    def clean_ai_score(self):
        ai_score = self.cleaned_data["ai_score"]
        if ai_score < 0 or ai_score > 100:
            raise forms.ValidationError(_("Score_must_be_between_0_and_100"))

        return ai_score
