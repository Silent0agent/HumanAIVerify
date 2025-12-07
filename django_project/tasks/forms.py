__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

import core.forms
import tasks.models


class TextTaskForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = tasks.models.TextTask
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


class AiScoreWidget(forms.NumberInput):
    template_name = "widgets/dual_range.html"

    class Media:
        js = ("js/dual_range_widget.js",)


class TaskCheckForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = tasks.models.TaskCheck
        fields = ["ai_score", "comment"]

        widgets = {
            "ai_score": AiScoreWidget(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "step": "0.1",
                    "placeholder": "0",
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

    def clean(self):
        instance = self.instance
        if (
            instance.pk
            and instance.status == tasks.models.TaskCheck.Status.PUBLISHED
        ):
            raise forms.ValidationError(_("Check_already_published"))

        return super().clean()
