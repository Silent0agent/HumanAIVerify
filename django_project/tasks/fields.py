__all__ = ()

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def make_client_field(prefix):
    return models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name=f"{prefix}_tasks",
        related_query_name=f"{prefix}_task",
        verbose_name=_("client"),
    )
