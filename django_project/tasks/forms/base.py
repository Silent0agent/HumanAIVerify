__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

import core.forms
import tasks.models.base


class BaseTaskForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        base_task_model = tasks.models.base.BaseTask
        fields = [
            base_task_model.title.field.name,
            base_task_model.description.field.name,
        ]

        labels = {
            base_task_model.title.field.name: _("Title"),
            base_task_model.description.field.name: _("Description"),
        }


class AiScoreWidget(forms.NumberInput):
    template_name = "widgets/dual_range.html"

    class Media:
        js = ("js/dual_range_widget.js",)


class BaseTaskCheckForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        base_check_model = tasks.models.base.BaseTaskCheck
        fields = [
            base_check_model.ai_score.field.name,
            base_check_model.comment.field.name,
        ]

        widgets = {
            base_check_model.ai_score.field.name: AiScoreWidget(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "step": "0.1",
                    "placeholder": "0",
                },
            ),
            base_check_model.comment.field.name: forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Your_comment_is_optional"),
                },
            ),
        }

        labels = {
            base_check_model.ai_score.field.name: _("AI_Probability_percent"),
            base_check_model.comment.field.name: _("Comment"),
        }

        help_texts = {
            base_check_model.ai_score.field.name: _("Enter_ai_percentage"),
        }

    def clean(self):
        instance = self.instance
        if (
            instance.pk
            and instance.status == instance.__class__.Status.PUBLISHED
        ):
            raise forms.ValidationError(_("Error_check_already_published"))

        return super().clean()
