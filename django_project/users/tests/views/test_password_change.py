__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.contrib.messages import constants as message_constants
from django.test import TestCase
from django.urls import reverse

User = auth.get_user_model()


class PasswordChangeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.password_change_url = reverse('auth:change-password')
        cls.raw_user_password = 'S3cure_P@ssw0rd!'
        cls.new_password = 'Pa$$word123'

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password=self.raw_user_password,
            is_active=True,
        )
        self.client.force_login(self.user)

    def test_change_password_loads(self):
        response = self.client.get(self.password_change_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_change.html')

    def test_change_password_view_status_code_found(self):
        response = self.client.post(
            self.password_change_url,
            {
                'old_password': self.raw_user_password,
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_change_password_view_redirects_to_login_view(self):
        response = self.client.post(
            self.password_change_url,
            {
                'old_password': self.raw_user_password,
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
        )
        self.assertRedirects(response, reverse('auth:login'))

    def test_change_password_view_changes_password(self):
        self.client.post(
            self.password_change_url,
            {
                'old_password': self.raw_user_password,
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

    def test_change_password_does_not_change_other_user_password(self):
        other_user_password = 'other_secret_password'
        other_user = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password=other_user_password,
        )
        self.client.post(
            self.password_change_url,
            {
                'old_password': self.raw_user_password,
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
        )

        other_user.refresh_from_db()
        self.assertTrue(other_user.check_password(other_user_password))

    def test_change_password_success_message(self):
        response = self.client.post(
            self.password_change_url,
            {
                'old_password': self.raw_user_password,
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
            follow=True,
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, message_constants.SUCCESS)

    def test_change_password_failure(self):
        response = self.client.post(
            self.password_change_url,
            {
                'old_password': 'wrong',
                'new_password1': self.new_password,
                'new_password2': self.new_password,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(self.user.check_password(self.raw_user_password))
