__all__ = ()

from django.contrib.auth import views as django_auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse

import users.views


class AuthRoutesTest(SimpleTestCase):
    def test_login(self):
        url = reverse("auth:login")
        self.assertEqual(url, "/auth/login/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.LoginView)

    def test_logout(self):
        url = reverse("auth:logout")
        self.assertEqual(url, "/auth/logout/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.LogoutView)

    def test_signup(self):
        url = reverse("auth:signup")
        self.assertEqual(url, "/auth/signup/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.SignUpView)

    def test_activate(self):
        url = reverse(
            "auth:activate",
            kwargs={"signed_username": "test_signature"},
        )
        self.assertEqual(url, "/auth/activate/test_signature/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            users.views.SignedUserActionView,
        )

    def test_unlock_account(self):
        url = reverse(
            "auth:unlock-account",
            kwargs={"signed_username": "test_signature"},
        )
        self.assertEqual(url, "/auth/unlock-account/test_signature/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            users.views.SignedUserActionView,
        )

    def test_change_password(self):
        url = reverse("auth:change-password")
        self.assertEqual(url, "/auth/change-password/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            users.views.PasswordChangeView,
        )

    def test_reset_password(self):
        url = reverse("auth:reset-password")
        self.assertEqual(url, "/auth/reset-password/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            users.views.PasswordResetView,
        )

    def test_password_reset_done(self):
        url = reverse("auth:password-reset-done")
        self.assertEqual(url, "/auth/reset-password/done/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            django_auth_views.PasswordResetDoneView,
        )

    def test_password_reset_confirm(self):
        url = reverse(
            "auth:password-reset-confirm",
            kwargs={"uidb64": "MQ", "token": "dummy-token"},
        )
        self.assertEqual(url, "/auth/reset-password/confirm/MQ/dummy-token/")

        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            users.views.PasswordResetConfirmView,
        )


class UsersRoutesTest(SimpleTestCase):
    def test_profile(self):
        url = reverse("users:profile")
        self.assertEqual(url, "/users/profile/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.ProfileView)

    def test_user_detail(self):
        url = reverse("users:user-detail", kwargs={"pk": 1})
        self.assertEqual(url, "/users/user-detail/1/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.UserDetailView)

    def test_set_role(self):
        url = reverse("users:set-role")
        self.assertEqual(url, "/users/set-role/")

        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, users.views.SetRoleView)
