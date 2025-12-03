__all__ = ()

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TextTask(models.Model):
    """Модель текстового задания для проверки ИИ."""

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("client"),
        related_name="text_tasks",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )

    class Meta:
        verbose_name = _("text task")
        verbose_name_plural = _("text tasks")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
