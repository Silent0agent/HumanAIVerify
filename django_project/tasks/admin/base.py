__all__ = ()

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BaseTaskAdmin(admin.ModelAdmin):
    unique_content_field = None
    content_display_method = None

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        client = self.model.client.field.name
        title = self.model.title.field.name
        desc = self.model.description.field.name
        created_at = self.model.created_at.field.name
        updated_at = self.model.updated_at.field.name

        content_name = self.unique_content_field.name

        list_content_col = self.content_display_method or content_name

        ai_score_method = "ai_score_display"
        get_task_str_method = "get_task_str"

        detail_content_fields = (content_name,)
        readonly_tuple = (ai_score_method, created_at, updated_at)

        if self.content_display_method:
            readonly_tuple += (self.content_display_method,)
            detail_content_fields = (content_name, self.content_display_method)

        self.list_display = (
            get_task_str_method,
            client,
            ai_score_method,
            list_content_col,
            created_at,
            updated_at,
        )

        self.list_filter = (created_at,)

        client_model = self.model.client.field.related_model
        client_email = client_model.email.field.name

        self.search_fields = (
            title,
            desc,
            client_email,
        )

        self.readonly_fields = readonly_tuple

        self.fieldsets = (
            (
                None,
                {
                    "fields": (
                        client,
                        title,
                        detail_content_fields,
                        desc,
                        ai_score_method,
                    ),
                },
            ),
            (
                _("Timestamps"),
                {
                    "fields": (created_at, updated_at),
                },
            ),
        )

    @admin.display(description=_("Average_AI_Score"))
    def ai_score_display(self, obj):
        value = obj.ai_score

        # Если значение None, пустая строка или False -> возвращаем текст
        if value is None:
            return _("No_checks")

        # Можно добавить форматирование
        return f"{value}%"

    @admin.display(description=_("Task"), ordering="title")
    def get_task_str(self, obj):
        return str(obj)


class BaseCheckAdmin(admin.ModelAdmin):
    unique_content_field = None

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        task = self.model.task.field.name
        performer = self.model.performer.field.name
        ai_score = self.model.ai_score.field.name
        status = self.model.status.field.name
        comment = self.model.comment.field.name
        created_at = self.model.created_at.field.name
        updated_at = self.model.updated_at.field.name

        unique_fields_tuple = ()
        if self.unique_content_field:
            unique_fields_tuple = (self.unique_content_field.name,)

        task_model = self.model.task.field.related_model
        task_title = task_model.title.field.name
        performer_model = self.model.performer.field.related_model
        performer_email = performer_model.email.field.name

        self.list_display = (
            task,
            performer,
            ai_score,
            status,
            created_at,
            updated_at,
        )

        self.list_filter = (status, created_at, ai_score)

        search_tuple = (
            f"{task}__{task_title}",
            f"{performer}__{performer_email}",
            comment,
        )

        self.search_fields = search_tuple

        self.readonly_fields = (created_at, updated_at)

        self.fieldsets = (
            (
                None,
                {
                    "fields": (
                        task,
                        performer,
                        status,
                        ai_score,
                    ),
                },
            ),
            (
                _("Content"),
                {
                    "fields": unique_fields_tuple + (comment,),
                },
            ),
            (
                _("Timestamps"),
                {
                    "fields": (created_at, updated_at),
                },
            ),
        )
