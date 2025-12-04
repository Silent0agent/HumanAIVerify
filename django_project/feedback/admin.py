__all__ = ()

from django.contrib import admin

import feedback.models


class FieldPaths:
    _author_field = feedback.models.Feedback.author.field.name
    _mail_field = feedback.models.FeedbackUserProfile.mail.field.name
    _name_field = feedback.models.FeedbackUserProfile.name.field.name

    FEEDBACK_AUTHOR_MAIL = f"{_author_field}__{_mail_field}"
    FEEDBACK_AUTHOR_NAME = f"{_author_field}__{_name_field}"


class FilesInline(admin.TabularInline):
    model = feedback.models.FeedbackFile


class FeedbackInline(admin.TabularInline):
    model = feedback.models.Feedback
    fields = (
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.text.field.name,
    )
    readonly_fields = fields
    can_delete = False


@admin.register(feedback.models.FeedbackUserProfile)
class FeedbackUserProfileAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.FeedbackUserProfile.mail.field.name,
        feedback.models.FeedbackUserProfile.name.field.name,
    )
    search_fields = (
        feedback.models.FeedbackUserProfile.mail.field.name,
        feedback.models.FeedbackUserProfile.name.field.name,
    )
    inlines = [FeedbackInline]


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.author.field.name,
        feedback.models.Feedback.status.field.name,
    )
    readonly_fields = (feedback.models.Feedback.created_on.field.name,)
    list_editable = (feedback.models.Feedback.status.field.name,)
    search_fields = (
        feedback.models.Feedback.text.field.name,
        FieldPaths.FEEDBACK_AUTHOR_MAIL,
        FieldPaths.FEEDBACK_AUTHOR_NAME,
    )
    inlines = (FilesInline,)

    def save_model(self, request, obj, form, change):
        field = feedback.models.Feedback.status.field.name
        if field in form.changed_data:
            feedback.models.StatusLog(
                user=request.user,
                feedback=obj,
                status_from=form.initial["status"],
                status_to=form.cleaned_data["status"],
            ).save()

        super().save_model(request, obj, form, change)


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.status_from.field.name,
        feedback.models.StatusLog.status_to.field.name,
    )
    readonly_fields = [
        field.name for field in feedback.models.StatusLog._meta.fields
    ]
