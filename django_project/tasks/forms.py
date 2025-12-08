__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

import core.forms
import tasks.models


class BaseTaskForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        fields = ["title", "description"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter_task_title"),
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _("Enter_task_description_optional"),
                },
            ),
        }

        labels = {
            "title": _("Title"),
            "description": _("Description"),
        }


class TextTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = tasks.models.TextTask
        fields = BaseTaskForm.Meta.fields + ["content"]

        widgets = {
            **BaseTaskForm.Meta.widgets,
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": _("Paste_text_for_AI_detection"),
                },
            ),
        }

        labels = {
            **BaseTaskForm.Meta.labels,
            "content": _("Content"),
        }


class AiScoreWidget(forms.NumberInput):
    template_name = "widgets/dual_range.html"

    class Media:
        js = ("js/dual_range_widget.js",)


class BaseTaskCheckForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
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
            and instance.status == instance.__class__.Status.PUBLISHED
        ):
            raise forms.ValidationError(_("Check_already_published"))

        return super().clean()


class TextTaskCheckForm(BaseTaskCheckForm):
    class Meta(BaseTaskCheckForm.Meta):
        model = tasks.models.TextTaskCheck
