__all__ = ()

from django.contrib import admin

from tasks.admin.base import BaseCheckAdmin, BaseCheckInline, BaseTaskAdmin
import tasks.models


class AudioCheckInline(BaseCheckInline):
    model = tasks.models.AudioTaskCheck


@admin.register(tasks.models.AudioTask)
class AudioTaskAdmin(BaseTaskAdmin):
    unique_content_field = tasks.models.AudioTask.audio.field
    content_display_method = tasks.models.AudioTask.audio_player.__name__
    check_model = tasks.models.AudioTaskCheck
    check_inline_class = AudioCheckInline


@admin.register(tasks.models.AudioTaskCheck)
class AudioTaskCheckAdmin(BaseCheckAdmin):
    unique_content_field = None
