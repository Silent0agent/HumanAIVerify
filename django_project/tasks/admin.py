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
    description_field = text_task_model.description.field.name
    created_at_field = text_task_model.created_at.field.name
    updated_at_field = text_task_model.updated_at.field.name

    ai_score_property = "ai_score"

    list_display = (
        title_field,
        client_field,
        ai_score_property,
        created_at_field,
        updated_at_field,
    )
    list_filter = (created_at_field,)
    search_fields = (
        title_field,
        content_field,
        description_field,
        f"{client_field_object}__{client_email}",
    )
    readonly_fields = (
        ai_score_property,
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
                    description_field,
                    ai_score_property,
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
            },
        ),
    )

    @admin.display(description=_("Average AI Score"))
    def ai_score(self, obj):
        return obj.ai_score


@admin.register(tasks.models.TextTaskCheck)
class TaskCheckAdmin(admin.ModelAdmin):
    task_check_model = tasks.models.TextTaskCheck

    task_field = task_check_model.task.field.name
    performer_field = task_check_model.performer.field.name
    ai_score_field = task_check_model.ai_score.field.name
    status_field = task_check_model.status.field.name
    comment_field = task_check_model.comment.field.name
    created_at_field = task_check_model.created_at.field.name
    updated_at_field = task_check_model.updated_at.field.name

    performer_email = (
        task_check_model.performer.field.related_model.email.field.name
    )
    task_title = task_check_model.task.field.related_model.title.field.name

    list_display = (
        task_field,
        performer_field,
        ai_score_field,
        status_field,
        created_at_field,
        updated_at_field,
    )

    list_filter = (
        status_field,
        created_at_field,
        ai_score_field,
    )

    search_fields = (
        f"{task_field}__{task_title}",
        f"{performer_field}__{performer_email}",
        comment_field,
    )

    readonly_fields = (
        created_at_field,
        updated_at_field,
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    task_field,
                    performer_field,
                    status_field,
                    ai_score_field,
                ),
            },
        ),
        (
            _("Content"),
            {
                "fields": (comment_field,),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    created_at_field,
                    updated_at_field,
                ),
            },
        ),
    )
