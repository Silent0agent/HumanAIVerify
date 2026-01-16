__all__ = ()

import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import core.validators
import tasks.fields
from tasks.models.base import BaseTask, BaseTaskCheck


class AudioTask(BaseTask):
    def audio_path(self, filename):
        extension = filename.split(".")[-1]
        return f"tasks/audio_tasks/{uuid.uuid4()}.{extension}"

    client = tasks.fields.make_task_client_field("audio")
    audio = models.FileField(
        verbose_name=_("audio_file"),
        upload_to=audio_path,
        validators=[
            FileExtensionValidator(["mp3", "wav"]),
            core.validators.FileSizeValidator(50 * 1024 * 1024),
        ],
    )

    class Meta(BaseTask.Meta):
        verbose_name = _("audio_task")
        verbose_name_plural = _("audio_tasks")

    def get_absolute_url(self):
        return reverse("tasks:audio-task-detail", kwargs={"task_id": self.pk})

    def audio_player(self):
        if self.audio:
            return mark_safe(
                f'<audio controls style="width: 250px; height: 40px;">'
                f'<source src="{self.audio.url}" type="audio/mpeg">'
                f'{_("Audio_not_supported_browser")}'
                f"</audio>",
            )

        return _("No_audio")

    audio_player.short_description = _("audio_preview")


class AudioTaskCheck(BaseTaskCheck):
    task = tasks.fields.make_check_task_field(AudioTask)
    performer = tasks.fields.make_check_performer_field("audio")

    class Meta(BaseTaskCheck.Meta):
        verbose_name = _("audio_task_check")
        verbose_name_plural = _("audio_task_checks")

    def get_absolute_url(self):
        return reverse(
            "tasks:audio-check-detail",
            kwargs={"check_id": self.pk},
        )
