__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.core import mail
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
            "password1": "S3cure_P@ssw0rd!",
            "password2": "S3cure_P@ssw0rd!",
        }

    def test_registration_view_loads(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_successful_registration_redirects_to_login(self):
        response = self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )

        self.assertRedirects(response, reverse("auth:login"))

    def test_successful_registration_creates_user(self):
        self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )

        user = User.objects.filter(
            username=self.valid_user_data["username"],
        ).first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)

    def test_successful_registration_sends_email(self):
        self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.valid_user_data["email"], mail.outbox[0].to)

    def test_registration_password_mismatch(self):
        data = self.valid_user_data.copy()
        data["password2"] = "WrongPassword"

        response = self.client.post(self.registration_url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context["form"]
        self.assertFalse(form.is_valid())

    def test_registration_duplicate_email_status_code_ok(self):
        User.objects.create_user(
            username="existing",
            email=self.valid_user_data["email"],
            password="password",
        )
        response = self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_registration_duplicate_email_does_not_create_user(self):
        User.objects.create_user(
            username="existing",
            email=self.valid_user_data["email"],
            password="password",
        )
        self.client.post(self.registration_url, data=self.valid_user_data)

        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_registration_duplicate_email_forme_rror(self):
        User.objects.create_user(
            username="existing",
            email=self.valid_user_data["email"],
            password="password",
        )
        response = self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )
        form = response.context["form"]

        self.assertIn("email", form.errors)
