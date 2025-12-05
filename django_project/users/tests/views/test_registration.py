__all__ = ()

from http import HTTPStatus
import unittest.mock

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

User = auth.get_user_model()


class RegistrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.registration_url = reverse("auth:signup")
        cls.valid_user_data = {
            "username": "testuser",
            "email": "test@email.com",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }

    def test_registration_view_loads(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/signup.html")

    @unittest.mock.patch("users.views.send_mail")
    def test_successful_registration(self, mock_send_mail):
        response = self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )
        self.assertRedirects(response, reverse("auth:login"))
        self.assertTrue(
            User.objects.filter(
                username=self.valid_user_data["username"],
            ).exists(),
        )
        mock_send_mail.assert_called_once()

    def test_registration_with_password_mismatch(self):
        mismatched_data = self.valid_user_data.copy()
        mismatched_data["password2"] = "MismatchedPassword"
        response = self.client.post(
            self.registration_url,
            data=mismatched_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
