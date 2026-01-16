__all__ = ()

from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete


def sorl_thumbnail_cleanup(**kwargs):
    delete(kwargs['file'])


cleanup_pre_delete.connect(sorl_thumbnail_cleanup)
