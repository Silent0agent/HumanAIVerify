__all__ = ()

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

import core.models
import tasks.managers


class BaseTask(core.models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    objects = tasks.managers.TaskQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return Truncator(self.title).chars(30)

    @property
    def ai_score(self):
        if hasattr(self, '_avg_ai_score'):
            return self._avg_ai_score

        return self.checks.get_avg_ai_score()


class BaseTaskCheck(core.models.TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('draft')
        PUBLISHED = 'published', _('published')

    ai_score = models.FloatField(
        verbose_name=_('ai_score'),
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    comment = models.TextField(
        verbose_name=_('comment'),
        blank=True,
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=15,
        default=Status.DRAFT,
        choices=Status.choices,
    )

    objects = tasks.managers.TaskCheckManager()

    class Meta:
        abstract = True
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(
                fields=['task', 'performer'],
                name='unique_%(class)s_performer',
            ),
        ]

    def __str__(self):
        task_title = Truncator(self.task.title).chars(20)
        return f'{task_title} | {self.performer.username} ({self.ai_score}%)'
