__all__ = ()

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TextTask(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="text_tasks",
        related_query_name="text_task",
        verbose_name=_("client"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated_at"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )

    class Meta:
        verbose_name = _("text_task")
        verbose_name_plural = _("text_tasks")
        ordering = ["-created_at"]

    def __str__(self):
        task_title = self.title
        if len(task_title) > 30:
            return task_title[:30] + "..."

        return task_title

    @property
    def ai_score(self):
        checks = self.checks.all()
        if not checks.exists():
            return None

        total_score = sum(check.ai_score for check in checks)
        return total_score / checks.count()


class TaskCheck(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("draft")
        PUBLISHED = "published", _("published")

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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated_at"),
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("status"),
    )

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
