__all__ = ()

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models
import tasks.fields
import tasks.managers
from tasks.models.base import BaseTask


class TextTask(BaseTask):
    client = tasks.fields.make_task_client_field("text")
<<<<<<< HEAD
    content = models.TextField(
=======
    content = CKEditor5Field(
        config_name="create_text_task_content",
>>>>>>> 179c09c (fix: tests, migrations, lint, highlighting text, models & forms logic)
        verbose_name=_("content"),
    )

    class Meta(BaseTask.Meta):
        verbose_name = _("text_task")
        verbose_name_plural = _("text_tasks")


class TextTaskCheck(core.models.TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("draft")
        PUBLISHED = "published", _("published")

<<<<<<< HEAD
=======
    annotated_content = models.TextField(
        blank=True,
        verbose_name=_("annotated_content"),
    )
>>>>>>> 179c09c (fix: tests, migrations, lint, highlighting text, models & forms logic)
    task = models.ForeignKey(
        TextTask,
        on_delete=models.CASCADE,
        related_name="checks",
        related_query_name="check",
        verbose_name=_("task"),
    )
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="task_checks",
        related_query_name="task_check",
        verbose_name=_("performer"),
    )
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
        verbose_name = _("task_check")
        verbose_name_plural = _("task_checks")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["task", "performer"],
                name="unique_task_performer",
            ),
        ]

    def __str__(self):
        task_title = self.task.title
        if len(task_title) > 20:
            task_title = task_title[:20] + "..."

        return (
            f"{self.task.title} | {self.performer.username} ({self.ai_score}%)"
        )
