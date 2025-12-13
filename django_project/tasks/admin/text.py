__all__ = ()

from django.contrib import admin

from tasks.admin.base import BaseCheckAdmin, BaseCheckInline, BaseTaskAdmin
import tasks.models


class TextCheckInline(BaseCheckInline):
    model = tasks.models.TextTaskCheck


@admin.register(tasks.models.TextTask)
class TextTaskAdmin(BaseTaskAdmin):
    unique_content_field = tasks.models.TextTask.content.field
    check_model = tasks.models.TextTaskCheck
    check_inline_class = TextCheckInline


@admin.register(tasks.models.TextTaskCheck)
class TextTaskCheckAdmin(BaseCheckAdmin):
    unique_content_field = tasks.models.TextTaskCheck.annotated_content.field
