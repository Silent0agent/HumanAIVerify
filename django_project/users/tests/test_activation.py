__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.core import signing
from django.test import TestCase
from django.urls import reverse

User = auth.get_user_model()


class UserActivationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signer = signing.TimestampSigner()

    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            email="testuser@example.com",
            is_active=False,
        )

    def test_successful_activation(self):
        signed_username = self.signer.sign(self.user.username)

        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": signed_username},
            ),
        )

        self.assertTemplateUsed(response, "users/activation_success.html")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activation_with_invalid_signature(self):
        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": "invalid_signature"},
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_activation_with_expired_signature(self):
        signed_username = self.signer.sign(self.user.username)
        expired_signature = f"{signed_username}:expired_part"

        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": expired_signature},
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
