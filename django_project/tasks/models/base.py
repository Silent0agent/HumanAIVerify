__all__ = ()

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models
import tasks.managers


class BaseTask(core.models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )

    objects = tasks.managers.TaskQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        task_title = self.title
        if len(task_title) > 30:
            return task_title[:30] + "..."

        return task_title

    @property
    def ai_score(self):
        if hasattr(self, "_avg_ai_score"):
            return self._avg_ai_score

        return self.checks.get_avg_ai_score()


class BaseTaskCheck(core.models.TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("draft")
        PUBLISHED = "published", _("published")

    ai_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name=_("ai_score"),
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("status"),
    )

    objects = tasks.managers.TaskCheckManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["task", "performer"],
                name="unique_%(class)s_performer",
            ),
        ]

    def __str__(self):
        task_title = self.task.title
        if len(task_title) > 20:
            task_title = task_title[:20] + "..."

        return (
            f"{self.task.title} | {self.performer.username} ({self.ai_score}%)"
        )
