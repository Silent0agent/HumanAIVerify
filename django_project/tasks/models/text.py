__all__ = ()

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

import tasks.fields
from tasks.models.base import BaseTask, BaseTaskCheck


class TextTask(BaseTask):
    client = tasks.fields.make_task_client_field("text")
    content = CKEditor5Field(
        verbose_name=_("content"),
        config_name="create_text_task_content",
    )

    class Meta(BaseTask.Meta):
        verbose_name = _("text_task")
        verbose_name_plural = _("text_tasks")

    def get_absolute_url(self):
        return reverse("tasks:text-task-detail", kwargs={"task_id": self.pk})


class TextTaskCheck(BaseTaskCheck):
    task = tasks.fields.make_check_task_field(TextTask)
    performer = tasks.fields.make_check_performer_field("text")
    annotated_content = models.TextField(
        verbose_name=_("annotated_content"),
        blank=True,
    )

    class Meta(BaseTaskCheck.Meta):
        verbose_name = _("text_task_check")
        verbose_name_plural = _("text_task_checks")

    def get_absolute_url(self):
        return reverse("tasks:text-check-detail", kwargs={"check_id": self.pk})
