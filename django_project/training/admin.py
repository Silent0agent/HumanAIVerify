__all__ = ()

from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

import training.models


@admin.register(training.models.TrainingText)
class TrainingTextAdmin(admin.ModelAdmin):
    list_display = ("id", "difficulty", "is_ai_generated", "content_preview")
    list_filter = ("difficulty", "is_ai_generated")
    search_fields = ("content",)
    list_per_page = 20

    fieldsets = (
        (
            _("Text_content"),
            {
                "fields": ("content", "explanation"),
            },
        ),
        (
            _("Classification"),
            {
                "fields": ("is_ai_generated", "difficulty"),
            },
        ),
    )

    def content_preview(self, obj):
        return Truncator(obj.content).chars(30)

    content_preview.short_description = _("Content_preview")


@admin.register(training.models.UserTrainingProgress)
class UserTrainingProgressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "training_score",
        "completed_count",
        "last_fail",
        "can_train_now",
    )
    list_filter = ("training_score",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at", "last_fail_timestamp")
    list_per_page = 20

    fieldsets = (
        (
            _("User_information"),
            {
                "fields": ("user", "training_score"),
            },
        ),
        (
            _("Training_status"),
            {
                "fields": ("last_fail_timestamp", "completed_texts"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    filter_horizontal = ("completed_texts",)

    def completed_count(self, obj):
        return obj.completed_texts.count()

    completed_count.short_description = _("Completed_texts")

    def last_fail(self, obj):
        if obj.last_fail_timestamp:
            time_diff = timezone.now() - obj.last_fail_timestamp
            if time_diff.days < 1:
                return _("hours_ago").format(hours=obj.remaining_hours)

            return timesince(obj.last_fail_timestamp)

        return _("Never")

    last_fail.short_description = _("Last_fail")

    def can_train_now(self, obj):
        return obj.can_take_test

    can_train_now.short_description = _("Can_train_now")
    can_train_now.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user", "training_score")

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        from django.contrib.auth.models import Group

        old_score = None
        if change and obj.pk:
            try:
                old_obj = training.models.UserTrainingProgress.objects.get(
                    pk=obj.pk,
                )
                old_score = old_obj.training_score
            except training.models.UserTrainingProgress.DoesNotExist:
                pass

        super().save_model(request, obj, form, change)

        if (
            old_score is not None
            and old_score < settings.TRAINING_COMPLETIONS_FOR_PERFORMER
            and obj.training_score
            >= settings.TRAINING_COMPLETIONS_FOR_PERFORMER
            and obj.user.role != "performer"
        ):
            performer_group, created = Group.objects.get_or_create(
                name="Performers",
            )
            obj.user.groups.add(performer_group)
            obj.user.role = "performer"
            obj.user.save()

            self.message_user(
                request,
                _("User_added_to_Performers_group"),
                level="SUCCESS",
            )
