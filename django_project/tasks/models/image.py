__all__ = ()

import uuid

from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import core.validators
import tasks.fields
from tasks.models.base import BaseTask, BaseTaskCheck


class ImageTask(BaseTask):
    def image_path(self, filename):
        extension = filename.split(".")[-1]
        return f"tasks/image_tasks/{uuid.uuid4()}.{extension}"

    client = tasks.fields.make_task_client_field("image")
    image = sorl.thumbnail.ImageField(
        verbose_name=_("image"),
        upload_to=image_path,
        validators=[core.validators.FileSizeValidator(50 * 1024 * 1024)],
    )

    class Meta(BaseTask.Meta):
        verbose_name = _("image_task")
        verbose_name_plural = _("image_tasks")


class ImageTaskCheck(BaseTaskCheck):
    task = tasks.fields.make_check_task_field(ImageTask)
    performer = tasks.fields.make_check_performer_field("image")

    class Meta(BaseTaskCheck.Meta):
        verbose_name = _("image_task_check")
        verbose_name_plural = _("image_task_checks")
