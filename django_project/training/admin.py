__all__ = ()

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

import core.paginators
import training.models


@admin.register(training.models.TrainingText)
class TrainingTextAdmin(admin.ModelAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    content_field = training.models.TrainingText.content.field
    is_ai_generated_field = training.models.TrainingText.is_ai_generated.field
    difficulty_field = training.models.TrainingText.difficulty.field
    explanation_field = training.models.TrainingText.explanation.field

    def content_preview(self, obj):
        return Truncator(obj.content).chars(30)

    content_preview.short_description = _("Content_preview")

    list_display = (
        content_preview.__name__,
        difficulty_field.name,
        is_ai_generated_field.name,
    )
    list_filter = (
        difficulty_field.name,
        is_ai_generated_field.name,
    )
    search_fields = (content_field.name,)

    fieldsets = (
        (
            _("Text_content"),
            {
                "fields": (
                    content_field.name,
                    explanation_field.name,
                ),
            },
        ),
        (
            _("Classification"),
            {
                "fields": (
                    is_ai_generated_field.name,
                    difficulty_field.name,
                ),
            },
        ),
    )


@admin.register(training.models.UserTrainingProgress)
class UserTrainingProgressAdmin(admin.ModelAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    user_field = training.models.UserTrainingProgress.user.field
    user_model = user_field.related_model
    training_score_field = (
        training.models.UserTrainingProgress.training_score.field
    )
    last_fail_field = (
        training.models.UserTrainingProgress.last_fail_timestamp.field
    )
    completed_texts_field = (
        training.models.UserTrainingProgress.completed_texts.field
    )
    created_at_field = training.models.UserTrainingProgress.created_at.field
    updated_at_field = training.models.UserTrainingProgress.updated_at.field

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

    list_display = (
        user_field.name,
        training_score_field.name,
        completed_count.__name__,
        last_fail.__name__,
        can_train_now.__name__,
    )

    list_filter = (training_score_field.name,)

    search_fields = (
        f"{user_field.name}__{user_model.username.field.name}",
        f"{user_field.name}__{user_model.email.field.name}",
    )

    readonly_fields = (
        created_at_field.name,
        updated_at_field.name,
        last_fail_field.name,
    )

    fieldsets = (
        (
            _("User_information"),
            {
                "fields": (
                    user_field.name,
                    training_score_field.name,
                ),
            },
        ),
        (
            _("Training_status"),
            {
                "fields": (
                    last_fail_field.name,
                    completed_texts_field.name,
                ),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    created_at_field.name,
                    updated_at_field.name,
                ),
            },
        ),
    )

    filter_horizontal = (completed_texts_field.name,)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                self.user_field.name,
                self.training_score_field.name,
            )

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
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
            and obj.user.role != self.user_model.Role.PERFORMER
        ):
            performer_group, created = Group.objects.get_or_create(
                name=settings.PERFORMER_GROUP_NAME,
            )
            obj.user.groups.add(performer_group)
            obj.user.role = self.user_model.Role.PERFORMER
            obj.user.save()

            self.message_user(
                request,
                _("User_added_to_performers_group"),
                level=messages.SUCCESS,
            )
