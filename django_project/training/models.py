__all__ = ()

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

import core.models
import training.managers


class TrainingText(core.models.TimeStampedModel):
    class Difficulty(models.TextChoices):
        EASY = "easy", _("easy")
        MEDIUM = "medium", _("medium")
        HARD = "hard", _("hard")

    content = models.TextField(
        verbose_name=_("content"),
    )
    is_ai_generated = models.BooleanField(
        verbose_name=_("is_ai_generated"),
        help_text=_("Is_the_text_AI_generated"),
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
        verbose_name=_("difficulty"),
    )
    explanation = models.TextField(
        blank=True,
        verbose_name=_("explanation"),
        help_text=_("Explanation_why_text_is_AI_or_human"),
    )

    class Meta:
        verbose_name = _("training_text")
        verbose_name_plural = _("training_texts")
        ordering = ["difficulty", "id"]

    def __str__(self):
        return Truncator(self.content).chars(30)


class UserTrainingProgress(core.models.TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="training_progress",
        verbose_name=_("user"),
    )
    training_score = models.IntegerField(
        default=0,
        verbose_name=_("training_score"),
        help_text=_("Current_training_score"),
    )
    last_fail_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("last_fail_timestamp"),
        help_text=_("Timestamp_of_last_failed_attempt"),
    )
    completed_texts = models.ManyToManyField(
        TrainingText,
        blank=True,
        related_name="completed_by_users",
        verbose_name=_("completed_texts"),
    )

    objects = training.managers.TrainingProgressQuerySet.as_manager()

    class Meta:
        verbose_name = _("user_training_progress")
        verbose_name_plural = _("user_training_progresses")

    def __str__(self):
        return self.user.username

    @property
    def can_take_test(self):
        if not self.last_fail_timestamp:
            return True

        time_since_fail = timezone.now() - self.last_fail_timestamp
        return time_since_fail.days >= 1

    @property
    def remaining_hours(self):
        if not self.last_fail_timestamp or self.can_take_test:
            return 0

        time_since_fail = timezone.now() - self.last_fail_timestamp
        return max(0, 24 - int(time_since_fail.total_seconds() / 3600))

    def add_completed_text(self, training_text, is_correct):
        self.completed_texts.add(training_text)

        if is_correct:
            self.training_score += 1
            self.last_fail_timestamp = None
        else:
            self.training_score = max(0, self.training_score - 2)
            self.last_fail_timestamp = timezone.now()

        self.save()

        if self.training_score >= settings.TRAINING_COMPLETIONS_FOR_PERFORMER:
            group_model = self.user.groups.model

            performer_group, created = group_model.objects.get_or_create(
                name=settings.PERFORMER_GROUP_NAME,
            )
            self.user.groups.add(performer_group)

            user_model = self.user._meta.model
            self.user.role = user_model.Role.PERFORMER
            self.user.save()

    def get_available_texts(self):
        return TrainingText.objects.exclude(
            id__in=self.completed_texts.values_list("id", flat=True),
        )
