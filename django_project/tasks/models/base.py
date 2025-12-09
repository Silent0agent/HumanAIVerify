__all__ = ()

from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models


class BaseTask(core.models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )

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
        return self.checks.get_avg_ai_score()
