__all__ = ()

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import tasks.models


@admin.register(tasks.models.TextTask)
class TextTaskAdmin(admin.ModelAdmin):
    text_task_model = tasks.models.TextTask

    client_field_object = text_task_model.client.field
    client_email = client_field_object.related_model.email.field.name

    client_field = client_field_object.name
    title_field = text_task_model.title.field.name
    content_field = text_task_model.content.field.name
    created_at_field = text_task_model.created_at.field.name
    updated_at_field = text_task_model.updated_at.field.name

    list_display = (
        title_field,
        client_field,
        created_at_field,
        created_at_field,
    )
    list_filter = (created_at_field,)
    search_fields = (
        title_field,
        content_field,
        f"{client_field_object}__{client_email}",
    )
    readonly_fields = (
        text_task_model.created_at.field.name,
        text_task_model.updated_at.field.name,
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    client_field,
                    title_field,
                    content_field,
                ),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    created_at_field,
                    updated_at_field,
                ),
                "classes": ("collapse",),
            },
        ),
    )
