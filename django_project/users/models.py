__all__ = ()

import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import core.validators
import users.managers


class AvatarFieldMixin(models.Model):
    def avatar_path(self, filename):
        extension = filename.split(".")[-1]
        return f"users/avatars/{uuid.uuid4()}.{extension}"

    avatar = sorl.thumbnail.ImageField(
        verbose_name=_("avatar"),
        upload_to=avatar_path,
        null=True,
        blank=True,
        validators=[core.validators.FileSizeValidator(5 * 1024 * 1024)],
    )

    class Meta:
        abstract = True

    def get_avatar_x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.avatar,
            "50x50",
            crop="center",
            upscale=True,
            quality=99,
        )

    def avatar_tmb(self):
        if self.avatar:
            return mark_safe(
                f"<img src='{self.get_avatar_x50().url}' "
                f"width='50' height='50'/>",
            )

        return _("no_avatar")

    avatar_tmb.short_description = _("avatar_preview")


class CustomUser(AvatarFieldMixin, AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", _("customer")
        PERFORMER = "performer", _("performer")

    email = models.EmailField(
        _("email"),
        unique=True,
    )

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    login_attempts_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("login_attempts_count"),
    )
    block_timestamp = models.DateTimeField(
        verbose_name=_("blocking_timestamp"),
        null=True,
    )
    last_login_attempt_timestamp = models.DateTimeField(
        verbose_name=_("last_login_attempt_timestamp"),
        null=True,
    )

    objects = users.managers.CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self._normalize_email_field()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        self._normalize_email_field()

    def _normalize_email_field(self):
        self.email = self.__class__.objects.normalize_email(self.email)


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural
