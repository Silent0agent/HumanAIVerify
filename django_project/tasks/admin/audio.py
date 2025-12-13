__all__ = ()

from django.contrib import admin

from tasks.admin.base import BaseCheckAdmin, BaseTaskAdmin
import tasks.models


@admin.register(tasks.models.AudioTask)
class AudioTaskAdmin(BaseTaskAdmin):
    unique_content_field = tasks.models.AudioTask.audio.field
    content_display_method = tasks.models.AudioTask.audio_player.__name__


@admin.register(tasks.models.AudioTaskCheck)
class AudioTaskCheckAdmin(BaseCheckAdmin):
    unique_content_field = None
