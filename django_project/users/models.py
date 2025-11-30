__all__ = ()

import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import users.managers


class CustomUser(AbstractUser):
    objects = users.managers.CustomUserManager()

    def avatar_path(self, filename):
        ext = filename.split(".")[-1]
        return f"users/avatars/{uuid.uuid4()}.{ext}"

    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to=avatar_path,
        null=True,
        blank=True,
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

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self._normalize_email_field()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self._normalize_email_field()

        if self.email:
            queryset = self.__class__.objects.filter(email=self.email)

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            if queryset.exists():
                raise ValidationError(
                    _("User_with_this_email_already_exists"),
                )

    def _normalize_email_field(self):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural
