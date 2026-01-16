__all__ = ()

from django.contrib import auth
from django.test import override_settings, TestCase

User = auth.get_user_model()


class UserLockoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword',
            is_active=True,
        )

    def test_profile_attempts_count(self):
        user = auth.authenticate(username='testuser', password='badpassword')
        self.assertIsNone(user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.login_attempts_count, 1)

    def test_login_resets_attempts(self):
        self.user.login_attempts_count = 2
        self.user.save()
        user = auth.authenticate(username='testuser', password='testpassword')
        self.user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(self.user.login_attempts_count, 0)

    @override_settings(MAX_AUTH_ATTEMPTS=1)
    def test_lockout_after_max_attempts(self):
        auth.authenticate(username='testuser', password='badpassword')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
