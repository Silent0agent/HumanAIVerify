__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.forms.base import BaseTaskCheckForm, BaseTaskForm
import tasks.models


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


class TextTaskCheckForm(BaseTaskCheckForm):
    class Meta(BaseTaskCheckForm.Meta):
        model = tasks.models.TextTaskCheck
