__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.contrib.messages import constants as message_constants
from django.core import signing
from django.test import override_settings, TestCase
from django.urls import reverse

User = auth.get_user_model()


class LoginTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.login_url = reverse("auth:login")
        cls.raw_user_password = "S3cure_P@ssw0rd!"
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=cls.raw_user_password,
            is_active=True,
        )

    def test_login_view_loads(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_with_username(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": self.raw_user_password,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_email(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.email,
                "password": self.raw_user_password,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_redirects_to_profile(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": self.raw_user_password,
            },
        )

        self.assertRedirects(response, reverse("users:profile"))

    @override_settings(MAX_AUTH_ATTEMPTS=1)
    def test_login_lockout_view_loads(self):
        self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "wrong",
            },
        )

        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "correct_or_wrong",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

    @override_settings(MAX_AUTH_ATTEMPTS=1)
    def test_login_lockout_message(self):
        self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "wrong",
            },
        )

        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "correct_or_wrong",
            },
        )

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, message_constants.WARNING)

    def test_unlock_account_status_code_ok(self):
        signer = signing.TimestampSigner()
        url = reverse(
            "auth:unlock-account",
            kwargs={"signed_username": signer.sign(self.user.username)},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unlock_account_template(self):
        signer = signing.TimestampSigner()
        url = reverse(
            "auth:unlock-account",
            kwargs={"signed_username": signer.sign(self.user.username)},
        )
        response = self.client.get(url)

        self.assertTemplateUsed(response, "users/activation_success.html")
