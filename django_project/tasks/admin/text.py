__all__ = ()

from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

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

    class Media:
        css = {'all': ('css/highlight_text.css',)}

    @admin.display(description=_('Annotated_content'), empty_value='-')
    def display_annotated_content(self, obj):
        content = obj.annotated_content
        if not content:
            return None

        return mark_safe(content)

    content_display_method = display_annotated_content.__name__
