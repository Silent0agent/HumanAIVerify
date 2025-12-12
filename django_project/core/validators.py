__all__ = ()

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            limit_mb = self.max_size / (1024 * 1024)
            raise ValidationError(
                _("max_size_limit") + str(round(limit_mb, 1)),
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator)
            and self.max_size == other.max_size
        )
