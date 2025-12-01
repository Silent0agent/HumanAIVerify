__all__ = ()

import importlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = _("core_app_name")

    def ready(self):
        importlib.import_module("core.signals")
