__all__ = ()

from django.db import models
from django.utils.translation import gettext_lazy as _

import tasks.fields
from tasks.models.base import BaseTask, BaseTaskCheck


class TextTask(BaseTask):
    client = tasks.fields.make_task_client_field("text")
    content = models.TextField(
        verbose_name=_("content"),
    )

    class Meta(BaseTask.Meta):
        verbose_name = _("text_task")
        verbose_name_plural = _("text_tasks")


class TextTaskCheck(BaseTaskCheck):
    task = tasks.fields.make_check_task_field(TextTask)
    performer = tasks.fields.make_check_performer_field("text")

    class Meta(BaseTaskCheck.Meta):
        verbose_name = _("text_task_check")
        verbose_name_plural = _("text_task_checks")
