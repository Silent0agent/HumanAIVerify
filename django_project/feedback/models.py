__all__ = ()

import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    RECEIVED = "received", _("received")
    IN_PROGRESS = "pending", _("pending")
    ANSWERED = "answered", _("answered")


class FeedbackUserProfile(models.Model):
    name = models.CharField(
        _("name"),
        max_length=150,
        help_text=_("max_symbols_help_text"),
        blank=True,
        null=True,
    )
    mail = models.EmailField(
        _("email"),
        help_text=_("email_help_text"),
    )

    class Meta:
        verbose_name = _("sender_contact_data")
        verbose_name_plural = _("sender_contact_data_plural")

    def __str__(self):
        return self.mail


class Feedback(models.Model):
    author = models.ForeignKey(
        FeedbackUserProfile,
        on_delete=models.SET_NULL,
        verbose_name=_("author"),
        related_name="feedbacks",
        null=True,
        blank=True,
    )

    text = models.TextField(
        _("feedback_text"),
        help_text=_("feedback_text_help_text"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
    )

    status = models.CharField(
        verbose_name=_("feedback_status"),
        help_text=_("status_help_text"),
        max_length=11,
        choices=StatusChoices,
        default=StatusChoices.RECEIVED,
    )

    class Meta:
        verbose_name = _("feedback")
        verbose_name_plural = _("feedback_plural")

    def __str__(self):
        return f"{self.text[:12]}..."


class FeedbackFile(models.Model):
    def file_path(self, filename):
        extension = filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{extension}"
        return f"feedback/attachments/{self.feedback_id}/{new_filename}"

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("feedback"),
    )
    file = models.FileField(
        upload_to=file_path,
        null=True,
        blank=True,
        verbose_name=_("feedback_file"),
    )

    class Meta:
        verbose_name = _("feedback_file")
        verbose_name_plural = _("feedback_file_plural")

    def __str__(self):
        return f"Id {self.id}"


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("user"),
    )
    feedback = models.ForeignKey(
        Feedback,
        verbose_name=_("feedback"),
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.TimeField(
        auto_now_add=True,
        verbose_name=_("time"),
    )
    status_from = models.CharField(
        choices=StatusChoices,
        db_column="from",
        max_length=11,
        verbose_name=_("status_from"),
    )
    status_to = models.CharField(
        choices=StatusChoices,
        db_column="to",
        max_length=11,
        verbose_name=_("status_to"),
    )

    class Meta:
        verbose_name = _("status_log")
        verbose_name_plural = _("status_log_plural")

    def __str__(self):
        return self.feedback.__str__()
