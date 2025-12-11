__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

import core.forms


class BaseTaskForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        fields = ["title", "description"]

        labels = {
            "title": _("Title"),
            "description": _("Description"),
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
                    "placeholder": _("your_comments_optional"),
                },
            ),
        }

        labels = {
            "ai_score": _("AI_Probability_percent"),
            "comment": _("Comments"),
        }

        help_texts = {
            "ai_score": _("enter_ai_percentage"),
        }

    def clean(self):
        instance = self.instance
        if (
            instance.pk
            and instance.status == instance.__class__.Status.PUBLISHED
        ):
            raise forms.ValidationError(_("check_already_published"))

        return super().clean()
