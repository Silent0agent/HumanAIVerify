__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = auth.get_user_model()


class PasswordResetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.password_reset_url = reverse("auth:reset-password")
        cls.password_reset_done_url = reverse("auth:password-reset-done")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="S3cure_P@ssw0rd!",
            is_active=True,
        )

    def test_password_reset_view_loads(self):
        response = self.client.get(self.password_reset_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/password_reset.html")

    def test_password_reset_status_code_found(self):
        response = self.client.post(
            self.password_reset_url,
            {"email": self.user.email},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_password_reset_redirects_to_password_reset_done(self):
        response = self.client.post(
            self.password_reset_url,
            {"email": self.user.email},
        )

        self.assertRedirects(response, self.password_reset_done_url)

    def test_password_reset_done_template(self):
        response = self.client.post(
            self.password_reset_url,
            {"email": self.user.email},
            follow=True,
        )

        self.assertTemplateUsed(response, "users/password_reset_done.html")

    def test_password_reset_sends_email_successfully(self):
        self.client.post(
            self.password_reset_url,
            {"email": self.user.email},
        )

        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn(self.user.email, sent_email.to)

    def test_password_reset_unknown_email(self):
        response = self.client.post(
            self.password_reset_url,
            {"email": "unknown@email.com"},
        )
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_does_not_send_email_to_other_user(self):
        User.objects.create_user(
            username="other",
            email="other@email.com",
            password="other_password",
        )

        self.client.post(
            self.password_reset_url,
            {"email": self.user.email},
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user.email, mail.outbox[0].to)


class PasswordResetConfirmTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.login_url = reverse(
            "auth:login",
        )
        cls.user_old_password = "old_password"
        cls.user_new_password = "Pa$$word123"

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password=self.user_old_password,
        )

    def _get_reset_url(self, user, token=None):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        if token is None:
            token = auth.tokens.default_token_generator.make_token(user)

        return reverse(
            "auth:password-reset-confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )

    def test_password_reset_confirm_page_loads(self):
        url = self._get_reset_url(self.user)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/password_reset_confirm.html")
        self.assertTrue(response.context["validlink"])

    def test_password_reset_confirm_invalid_token(self):
        url = self._get_reset_url(self.user, token="fake-token")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/password_reset_confirm.html")
        self.assertFalse(response.context["validlink"])

    def test_password_reset_confirm_success_status_code_found(self):
        url = self._get_reset_url(self.user)
        response_get = self.client.get(url, follow=True)
        target_url = response_get.request["PATH_INFO"]

        response = self.client.post(
            target_url,
            {
                "new_password1": self.user_new_password,
                "new_password2": self.user_new_password,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_password_reset_confirm_success_redirects_to_login(self):
        url = self._get_reset_url(self.user)
        response_get = self.client.get(url, follow=True)
        target_url = response_get.request["PATH_INFO"]

        response = self.client.post(
            target_url,
            {
                "new_password1": self.user_new_password,
                "new_password2": self.user_new_password,
            },
        )

        self.assertRedirects(response, self.login_url)

    def test_reset_complete_template(self):
        url = self._get_reset_url(self.user)
        response_get = self.client.get(url, follow=True)
        target_url = response_get.request["PATH_INFO"]

        response = self.client.post(
            target_url,
            {
                "new_password1": self.user_new_password,
                "new_password2": self.user_new_password,
            },
            follow=True,
        )

        self.assertTemplateUsed(response, "users/login.html")

    def test_password_reset_confirm_success_changes_password(self):
        url = self._get_reset_url(self.user)
        response_get = self.client.get(url, follow=True)
        target_url = response_get.request["PATH_INFO"]

        self.client.post(
            target_url,
            {
                "new_password1": self.user_new_password,
                "new_password2": self.user_new_password,
            },
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.user_new_password))

    def test_password_reset_complete_mismatch_passwords(self):
        url = self._get_reset_url(self.user)
        response_get = self.client.get(url, follow=True)
        target_url = response_get.request["PATH_INFO"]

        response = self.client.post(
            target_url,
            {
                "new_password1": "Pa$$word123",
                "new_password2": "Pa$$word987",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.user_old_password))
