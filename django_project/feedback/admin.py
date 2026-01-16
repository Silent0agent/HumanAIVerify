__all__ = ()

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import core.paginators
import feedback.models


class FieldPaths:
    author_field = feedback.models.Feedback.author.field.name
    mail_field = feedback.models.FeedbackUserProfile.mail.field.name
    name_field = feedback.models.FeedbackUserProfile.name.field.name

    FEEDBACK_AUTHOR_MAIL = f'{author_field}__{mail_field}'
    FEEDBACK_AUTHOR_NAME = f'{author_field}__{name_field}'


class FilesInline(admin.TabularInline):
    model = feedback.models.FeedbackFile

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(self.model.feedback.field.name)


class FeedbackInline(admin.TabularInline):
    model = feedback.models.Feedback
    can_delete = False
    extra = 0

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        created_at = self.model.created_at.field.name
        status = self.model.status.field.name

        str_method = self.get_feedback_str.__name__

        self.fields = (created_at, status, str_method)
        self.readonly_fields = (created_at, str_method)

    @admin.display(description=_('Text'))
    def get_feedback_str(self, obj):
        return str(obj)


@admin.register(feedback.models.FeedbackUserProfile)
class FeedbackUserProfileAdmin(admin.ModelAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    list_display = (
        feedback.models.FeedbackUserProfile.mail.field.name,
        feedback.models.FeedbackUserProfile.name.field.name,
    )
    search_fields = (
        feedback.models.FeedbackUserProfile.mail.field.name,
        feedback.models.FeedbackUserProfile.name.field.name,
    )
    inlines = (FeedbackInline,)


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    list_display = (
        feedback.models.Feedback.created_at.field.name,
        feedback.models.Feedback.author.field.name,
        feedback.models.Feedback.status.field.name,
    )
    readonly_fields = (feedback.models.Feedback.created_at.field.name,)
    list_editable = (feedback.models.Feedback.status.field.name,)
    search_fields = (
        feedback.models.Feedback.text.field.name,
        FieldPaths.FEEDBACK_AUTHOR_MAIL,
        FieldPaths.FEEDBACK_AUTHOR_NAME,
    )
    inlines = (FilesInline,)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(feedback.models.Feedback.author.field.name)
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        status_field = feedback.models.Feedback.status.field
        field_name = status_field.name

        if field_name in form.changed_data:
            if change:
                status_from = form.initial.get(field_name)
            else:
                status_from = status_field.get_default()

            feedback.models.StatusLog(
                user=request.user,
                feedback=obj,
                status_from=status_from,
                status_to=obj.status,
            ).save()


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.status_from.field.name,
        feedback.models.StatusLog.status_to.field.name,
    )
    readonly_fields = [field.name for field in feedback.models.StatusLog._meta.fields]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                self.model.user.field.name,
                self.model.feedback.field.name,
            )
        )
