__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.forms.base import BaseTaskCheckForm, BaseTaskForm
import tasks.models


class AudioTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = tasks.models.AudioTask

        audio_field = tasks.models.AudioTask.audio.field.name

        fields = BaseTaskForm.Meta.fields + [
            audio_field,
        ]
        widgets = {
            audio_field: forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".mp3, .wav",
                },
            ),
        }
        labels = {
            **BaseTaskForm.Meta.labels,
            audio_field: _("Audio_file"),
        }


class AudioTaskCheckForm(BaseTaskCheckForm):
    class Meta(BaseTaskCheckForm.Meta):
        model = tasks.models.AudioTaskCheck
