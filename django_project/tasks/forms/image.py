__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.forms.base import BaseTaskCheckForm, BaseTaskForm
import tasks.models


class ImageTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = tasks.models.ImageTask
        fields = BaseTaskForm.Meta.fields + [model.image.field.name]

        widgets = {
            model.image.field.name: forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*',
                },
            ),
        }

        labels = {
            **BaseTaskForm.Meta.labels,
            model.image.field.name: _('Image'),
        }


class ImageTaskCheckForm(BaseTaskCheckForm):
    class Meta(BaseTaskCheckForm.Meta):
        model = tasks.models.ImageTaskCheck
