from django import forms
from django.utils.translation import gettext_lazy as _
from .models import TextTask, TaskCheck


class TextTaskForm(forms.ModelForm):
    class Meta:
        model = TextTask
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter task title"),
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": _("Paste text for AI detection"),
                }
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
                    "placeholder": _("0-100%"),
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Your comments (optional)"),
                }
            ),
        }

        labels = {
            "ai_score": _("AI Probability (%)"),
            "comment": _("Comments"),
        }

        help_texts = {
            "ai_score": _("Enter percentage from 0 to 100"),
        }

    def clean_ai_score(self):
        ai_score = self.cleaned_data["ai_score"]
        if ai_score < 0 or ai_score > 100:
            raise forms.ValidationError(_("Score must be between 0 and 100"))
        return ai_score
