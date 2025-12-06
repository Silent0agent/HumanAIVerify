__all__ = ()

from django.contrib.auth import get_user_model
from django.test import TestCase

import users.forms

User = get_user_model()


class SignUpFormTests(TestCase):
    def test_signup_form_email_uniqueness(self):
        email = "unique@example.com"
        User.objects.create_user(
            username="existing_user",
            email=email,
            password="test_password",
        )

        form_data = {
            "username": "new_user",
            "email": email,
            "password1": "S3cure_P@ssw0rd!",
            "password2": "S3cure_P@ssw0rd!",
        }
        form = users.forms.SignUpForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_signup_form_email_normalization_check(self):
        email = "test@example.com"
        User.objects.create_user(
            username="user1",
            email=email,
            password="password",
        )

        form_data = {
            "username": "user2",
            "email": "TeSt@ExAmPlE.CoM",
            "password1": "S3cure_P@ssw0rd!",
            "password2": "S3cure_P@ssw0rd!",
        }
        form = users.forms.SignUpForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_signup_form_valid_data(self):
        form_data = {
            "username": "valid_user",
            "email": "valid@example.com",
            "password1": "S3cure_P@ssw0rd!",
            "password2": "S3cure_P@ssw0rd!",
        }
        form = users.forms.SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())


class CustomAuthenticationFormTests(TestCase):
    def test_remember_me_field_exists(self):
        form = users.forms.LoginForm()
        self.assertIn("remember_me", form.fields)
        self.assertFalse(form.fields["remember_me"].required)


class UserProfileFormTests(TestCase):
    def test_profile_form_fields_exist(self):
        form = users.forms.UserProfileForm()
        expected_fields = ["avatar", "first_name", "last_name", "email"]

        self.assertEqual(len(form.fields), len(expected_fields))
        for field_name in expected_fields:
            with self.subTest(field=field_name):
                self.assertIn(field_name, form.fields)

    def test_profile_form_update(self):
        user = User.objects.create_user(
            username="profile_user",
            email="test@test.com",
            password="test_password",
        )

        data = {
            "first_name": "NewName",
            "last_name": "NewSurname",
            "email": "new_email@test.com",
        }

        form = users.forms.UserProfileForm(data=data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()

        user.refresh_from_db()
        self.assertEqual(user.first_name, "NewName")
        self.assertEqual(user.last_name, "NewSurname")
        self.assertEqual(user.email, "new_email@test.com")
