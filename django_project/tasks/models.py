all = ()

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TextTask(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="text_tasks",
        verbose_name=_("client"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    ai_score = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = _("text task")
        verbose_name_plural = _("text tasks")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def update_ai_score(self):
        checks = self.checks.all()
        if checks.exists():
            avg_score = (
                sum(check.ai_score for check in checks) / checks.count()
            )
            self.ai_score = avg_score
            self.save()


class TaskCheck(models.Model):
    task = models.ForeignKey(
        TextTask,
        on_delete=models.CASCADE,
        related_name="checks",
    )
    expert = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="task_checks",
        verbose_name=_("expert"),
    )
    ai_score = models.FloatField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("task check")
        verbose_name_plural = _("task checks")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Check {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.task.update_ai_score()
