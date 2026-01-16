__all__ = ()

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def make_task_client_field(prefix):
    return models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name=f'{prefix}_tasks',
        related_query_name=f'{prefix}_task',
        verbose_name=_('client'),
    )


def make_check_task_field(to_model):
    return models.ForeignKey(
        to_model,
        on_delete=models.CASCADE,
        related_name='checks',
        related_query_name='check',
        verbose_name=_('task'),
    )


def make_check_performer_field(prefix):
    return models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name=f'{prefix}_task_checks',
        related_query_name=f'{prefix}_task_check',
        verbose_name=_('performer'),
    )
