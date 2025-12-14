__all__ = ()

from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

import core.paginators


class BaseCheckInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    can_delete = False
    classes = ("collapse",)

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)

        self.created_at = self.model.created_at.field.name
        self.ai_score = self.model.ai_score.field.name
        self.status = self.model.status.field.name

        self.performer = self.model.performer.field.name
        self.performer_model = self.model.performer.field.related_model
        self.performer_email = self.performer_model.email.field.name
        self.performer_email_lookup = (
            f"{self.performer}__{self.performer_email}"
        )
        self.performer_username = self.performer_model.username.field.name
        self.performer_username_lookup = (
            f"{self.performer}__{self.performer_username}"
        )

        self.task = self.model.task.field.name
        self.task_model = self.model.task.field.related_model
        self.task_title = self.task_model.title.field.name
        self.task_title_lookup = f"{self.task}__{self.task_title}"

        self.performer_method = self.get_performer_email.__name__

        fields_list = (
            self.created_at,
            self.performer_method,
            self.ai_score,
            self.status,
        )

        self.readonly_fields = fields_list
        self.fields = fields_list

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs.with_performer()
            .with_task()
            .only(
                self.created_at,
                self.performer_email_lookup,
                self.ai_score,
                self.status,
                self.task_title_lookup,
                self.performer_username_lookup,
            )
        )

    @admin.display(description=_("Performer"), empty_value="-")
    def get_performer_email(self, obj):
        user = getattr(obj, self.model.performer.field.name)
        return user.email if user else None


class BaseTaskAdmin(admin.ModelAdmin):
    unique_content_field = None
    content_display_method = None
    check_model = None
    check_inline_class = None

    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    def __init__(self, model, admin_site):
        if self.check_model is None or self.unique_content_field is None:
            raise ImproperlyConfigured(
                _("Error_task_admin_improperly_configured")
                % {
                    "class_name": self.__class__.__name__,
                },
            )

        if self.check_inline_class:
            self.inlines = (self.check_inline_class,)

        super().__init__(model, admin_site)

        self.title = self.model.title.field.name
        self.description = self.model.description.field.name
        self.created_at = self.model.created_at.field.name
        self.updated_at = self.model.updated_at.field.name

        self.client = self.model.client.field.name
        self.client_model = self.model.client.field.related_model
        self.client_email = self.client_model.email.field.name
        self.client_email_lookup = f"{self.client}__{self.client_email}"

        self.content_name = self.unique_content_field.name

        ai_score_method = self.ai_score_display.__name__
        get_task_str_method = self.get_task_str.__name__

        detail_content_fields = (self.content_name,)
        readonly_tuple = (
            ai_score_method,
            self.created_at,
            self.updated_at,
            self.client,
        )

        list_display_tuple = (
            get_task_str_method,
            self.client,
            ai_score_method,
            self.created_at,
        )

        if self.content_display_method:
            readonly_tuple += (self.content_display_method,)
            list_display_tuple += (self.content_display_method,)
            detail_content_fields = (
                self.content_name,
                self.content_display_method,
            )

        self.list_display = list_display_tuple

        self.list_filter = (self.created_at,)

        self.search_fields = (
            self.title,
            self.description,
            self.client_email_lookup,
        )

        self.readonly_fields = readonly_tuple

        self.fieldsets = (
            (
                None,
                {
                    "fields": (
                        self.client,
                        self.title,
                        detail_content_fields,
                        self.description,
                        ai_score_method,
                    ),
                },
            ),
            (
                _("Timestamps"),
                {
                    "fields": (self.created_at, self.updated_at),
                },
            ),
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_url = request.resolver_match.url_name

        opts = self.model._meta
        changelist_url_name = f"{opts.app_label}_{opts.model_name}_changelist"
        qs = qs.with_client()

        if current_url == changelist_url_name:
            if self.check_model:
                qs = qs.with_avg_ai_score(self.check_model)

            fields_to_load = (
                self.title,
                self.client_email_lookup,
                self.created_at,
            )

            if self.content_display_method:
                fields_to_load += (self.unique_content_field.name,)

            return qs.only(*fields_to_load)

        if self.check_model:
            return qs.with_avg_ai_score(self.check_model)

        return qs

    @admin.display(description=_("Average_AI_Score"))
    def ai_score_display(self, obj):
        value = obj.ai_score
        if value is None:
            return _("No_checks")

        return f"{value}%"

    @admin.display(description=_("Task"), ordering="title")
    def get_task_str(self, obj):
        return str(obj)


class BaseCheckAdmin(admin.ModelAdmin):
    unique_content_field = None
    content_display_method = None

    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.ai_score = self.model.ai_score.field.name
        self.status = self.model.status.field.name
        self.comment = self.model.comment.field.name
        self.created_at = self.model.created_at.field.name
        self.updated_at = self.model.updated_at.field.name

        self.performer = self.model.performer.field.name
        self.performer_model = self.model.performer.field.related_model
        self.performer_email = self.performer_model.email.field.name
        self.performer_email_lookup = (
            f"{self.performer}__{self.performer_email}"
        )
        self.performer_username = self.performer_model.username.field.name
        self.performer_username_lookup = (
            f"{self.performer}__{self.performer_username}"
        )

        self.task = self.model.task.field.name
        self.task_model = self.model.task.field.related_model
        self.task_title = self.task_model.title.field.name
        self.task_title_lookup = f"{self.task}__{self.task_title}"

        self.list_display = (
            self.task,
            self.performer,
            self.ai_score,
            self.status,
            self.created_at,
            self.updated_at,
        )

        self.list_filter = (self.status, self.created_at)

        self.search_fields = (
            self.task_title_lookup,
            self.performer_email_lookup,
            self.comment,
        )

        readonly_tuple = (
            self.created_at,
            self.updated_at,
            self.task,
            self.performer,
        )

        if self.content_display_method:
            readonly_tuple += (self.content_display_method,)
            content_field_to_show = self.content_display_method
        elif self.unique_content_field:
            content_field_to_show = self.unique_content_field.name
        else:
            content_field_to_show = None

        self.readonly_fields = readonly_tuple

        content_fieldset_fields = (self.comment,)
        if content_field_to_show:
            content_fieldset_fields = (
                content_field_to_show,
            ) + content_fieldset_fields

        self.fieldsets = (
            (
                None,
                {
                    "fields": (
                        self.task,
                        self.performer,
                        self.status,
                        self.ai_score,
                    ),
                },
            ),
            (
                _("Content"),
                {
                    "fields": content_fieldset_fields,
                },
            ),
            (
                _("Timestamps"),
                {
                    "fields": (self.created_at, self.updated_at),
                },
            ),
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        current_url = request.resolver_match.url_name
        opts = self.model._meta
        changelist_url_name = f"{opts.app_label}_{opts.model_name}_changelist"
        qs = qs.with_task().with_performer()

        if current_url == changelist_url_name:
            fields_to_load = (
                self.ai_score,
                self.status,
                self.created_at,
                self.updated_at,
                self.task_title_lookup,
                self.performer_email_lookup,
                self.performer_username_lookup,
            )
            return qs.only(*fields_to_load)

        return qs
