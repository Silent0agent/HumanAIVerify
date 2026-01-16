__all__ = ()

import uuid

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import core.validators
import tasks.fields
from tasks.models.base import BaseTask, BaseTaskCheck


class ImageTask(BaseTask):
    def image_path(self, filename):
        extension = filename.split('.')[-1]
        return f'tasks/image_tasks/{uuid.uuid4()}.{extension}'

    client = tasks.fields.make_task_client_field('image')
    image = sorl.thumbnail.ImageField(
        verbose_name=_('image'),
        upload_to=image_path,
        validators=[core.validators.FileSizeValidator(50 * 1024 * 1024)],
    )

    class Meta(BaseTask.Meta):
        verbose_name = _('image_task')
        verbose_name_plural = _('image_tasks')

    def get_absolute_url(self):
        return reverse('tasks:image-task-detail', kwargs={'task_id': self.pk})

    def get_image_x150(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            '150x150',
            crop='center',
            upscale=True,
            quality=99,
        )

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.get_image_x150().url}" width="50" height="50"/>',
            )

        return _('No_image')

    image_tmb.short_description = _('image_preview')


class ImageTaskCheck(BaseTaskCheck):
    task = tasks.fields.make_check_task_field(ImageTask)
    performer = tasks.fields.make_check_performer_field('image')

    class Meta(BaseTaskCheck.Meta):
        verbose_name = _('image_task_check')
        verbose_name_plural = _('image_task_checks')

    def get_absolute_url(self):
        return reverse(
            'tasks:image-check-detail',
            kwargs={'check_id': self.pk},
        )
