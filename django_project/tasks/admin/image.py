__all__ = ()

from django.contrib import admin

from tasks.admin.base import BaseCheckAdmin, BaseCheckInline, BaseTaskAdmin
import tasks.models


class ImageCheckInline(BaseCheckInline):
    model = tasks.models.ImageTaskCheck


@admin.register(tasks.models.ImageTask)
class ImageTaskAdmin(BaseTaskAdmin):
    unique_content_field = tasks.models.ImageTask.image.field
    content_display_method = tasks.models.ImageTask.image_tmb.__name__
    check_model = tasks.models.ImageTaskCheck
    check_inline_class = ImageCheckInline


@admin.register(tasks.models.ImageTaskCheck)
class ImageTaskCheckAdmin(BaseCheckAdmin):
    unique_content_field = None
