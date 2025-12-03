__all__ = ()

from django.conf import settings
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
        return self.title
