__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.forms.base import BaseTaskCheckForm, BaseTaskForm
import tasks.models


class TextTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = tasks.models.TextTask
        fields = BaseTaskForm.Meta.fields + ["content"]

        labels = {
            **BaseTaskForm.Meta.labels,
            "content": _("Content") + " *",
        }


class TextTaskCheckForm(BaseTaskCheckForm):
    highlighted_content = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
    )

    class Meta(BaseTaskCheckForm.Meta):
        model = tasks.models.TextTaskCheck
        fields = ["highlighted_content"] + BaseTaskCheckForm.Meta.fields
