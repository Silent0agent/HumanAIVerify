__all__ = ()

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
