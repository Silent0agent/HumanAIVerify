__all__ = ()

import threading

from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import core.utils

User = auth.get_user_model()


class EmailBackend(auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = self._get_user(username)
        if not user:
            return None

        if not user.check_password(password):
            self._handle_failed_login(request, user)
            return None

        if not user.is_active:
            return None

        self._handle_successful_login(user)
        return user

    def _get_user(self, username):
        if not username:
            return None

        if '@' in username:
            return User.objects.by_mail(username)

        return User.objects.filter(username=username).first()

    def _handle_successful_login(self, user):
        user.login_attempts_count = 0
        user.block_timestamp = None
        user.last_login_attempt_timestamp = timezone.now()
        user.save()

    def _handle_failed_login(self, request, user):
        user.login_attempts_count += 1
        user.last_login_attempt_timestamp = timezone.now()

        if user.login_attempts_count >= settings.MAX_AUTH_ATTEMPTS:
            self._block_user(request, user)

        user.save()

    def _block_user(self, request, user):
        user.is_active = False
        user.block_timestamp = timezone.now()

        if request:
            messages.warning(
                request,
                _('Account_blocked_due_maxed_attempts'),
            )
            self._send_activation_email(request, user)

    def _send_activation_email(self, request, user):
        signer = signing.TimestampSigner()
        signed_username = signer.sign(user.username)

        activate_link = request.build_absolute_uri(
            reverse(
                'auth:unlock-account',
                kwargs={'signed_username': signed_username},
            ),
        )

        send_mail(
            subject=_('Profile_activation'),
            message=render_to_string(
                'users/subjects/activation_email.txt',
                {'activate_link': activate_link},
            ),
            from_email=settings.EMAIL_FROM_DEFAULT,
            recipient_list=[user.email],
        )
        threading.Thread(target=core.utils.send_mail_async).start()
