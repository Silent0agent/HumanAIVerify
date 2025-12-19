__all__ = ()

import uuid

from django.conf import settings
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

import core.models
import core.validators


class StatusChoices(models.TextChoices):
    RECEIVED = "received", _("received")
    IN_PROGRESS = "pending", _("pending")
    ANSWERED = "answered", _("answered")


class FeedbackUserProfile(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_("Maximum_characters") % {"max": 150},
    )
    mail = models.EmailField(
        verbose_name=_("email"),
        help_text=_("Email_help_text"),
    )

    class Meta:
        verbose_name = _("sender_contact_data")
        verbose_name_plural = _("sender_contact_data_plural")

    def __str__(self):
        return self.mail


class Feedback(core.models.TimeStampedModel):
    author = models.ForeignKey(
        FeedbackUserProfile,
        on_delete=models.SET_NULL,
        related_name="feedbacks",
        related_query_name="feedback",
        verbose_name=_("author"),
        blank=True,
        null=True,
    )

    text = models.TextField(
        _("feedback_text"),
        help_text=_("Feedback_text_help_text"),
    )

    status = models.CharField(
        verbose_name=_("feedback_status"),
        max_length=11,
        default=StatusChoices.RECEIVED,
        choices=StatusChoices,
        help_text=_("Status_help_text"),
    )

    class Meta:
        verbose_name = _("feedback")
        verbose_name_plural = _("feedback_plural")

    def __str__(self):
        return Truncator(self.text).chars(30)


class FeedbackFile(models.Model):
    def file_path(self, filename):
        extension = filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{extension}"
        return f"feedback/attachments/{self.feedback_id}/{new_filename}"

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
        verbose_name=_("feedback"),
    )
    file = models.FileField(
        verbose_name=_("feedback_file"),
        upload_to=file_path,
        blank=True,
        null=True,
        validators=[core.validators.FileSizeValidator(16 * 1024 * 1024)],
    )

    class Meta:
        verbose_name = _("feedback_file")
        verbose_name_plural = _("feedback_file_plural")

    def __str__(self):
        return self.feedback.__str__()


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="feedback_status_logs",
        related_query_name="feedback_status_log",
        verbose_name=_("user"),
        null=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.SET_NULL,
        related_name="status_logs",
        related_query_name="status_log",
        verbose_name=_("feedback"),
        null=True,
    )
    timestamp = models.TimeField(
        verbose_name=_("time"),
        auto_now_add=True,
    )
    status_from = models.CharField(
        verbose_name=_("status_from"),
        max_length=11,
        choices=StatusChoices,
        db_column="from",
    )
    status_to = models.CharField(
        verbose_name=_("status_to"),
        max_length=11,
        choices=StatusChoices,
        db_column="to",
    )

    class Meta:
        verbose_name = _("status_log")
        verbose_name_plural = _("status_log_plural")

    def __str__(self):
        return self.feedback.__str__()
