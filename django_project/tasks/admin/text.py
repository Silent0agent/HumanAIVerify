__all__ = ()

from django.contrib import admin

from tasks.admin.base import BaseCheckAdmin, BaseTaskAdmin
import tasks.models


@admin.register(tasks.models.TextTask)
class TextTaskAdmin(BaseTaskAdmin):
    unique_content_field = tasks.models.TextTask.content.field


@admin.register(tasks.models.TextTaskCheck)
class TextTaskCheckAdmin(BaseCheckAdmin):
    unique_content_field = None
