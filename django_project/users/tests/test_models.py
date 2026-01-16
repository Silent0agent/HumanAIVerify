__all__ = ()

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

User = auth.get_user_model()


class UserModelTests(TestCase):
    @parameterized.expand(
        [
            ("user@email.com", "user@email.com"),
            ("user+some+tag@email.com", "user@email.com"),
            ("UsER@email.com", "user@email.com"),
            ("u.se.r@gmail.com", "user@gmail.com"),
            ("user@ya.ru", "user@yandex.ru"),
            ("u.se.r@yandex.ru", "u-se-r@yandex.ru"),
        ],
    )
    def test_email_normalization(self, email, expected_normalized_email):
        user = User(username="normalization_test_user", email=email)
        user.save()

        self.assertEqual(user.email, expected_normalized_email)

    def test_user_default_role_customer(self):
        user = User.objects.create_user(
            username="role_test_user",
            email="role_test@email.com",
            password="testpassword",
            is_active=True,
        )

        self.assertEqual(user.role, User.Role.CUSTOMER)

    def test_avatar_path_generation(self):
        user = User(email="avatar_test@example.com")
        filename = "my_avatar.jpg"
        generated_path = user.avatar_path(filename)

        self.assertTrue(generated_path.startswith("users/avatars/"))
        self.assertTrue(generated_path.endswith(".jpg"))
        self.assertRegex(generated_path, r"^users/avatars/[a-f0-9-]{36}\.jpg$")

    def test_user_str_representation(self):
        email = "test@example.com"
        user = User(username="str_user", email=email)
        self.assertEqual(str(user), email)

    def test_get_absolute_url(self):
        user = User.objects.create_user(
            username="test user",
            email="test@example.com",
            password="testpassword",
        )
        expected_url = reverse("users:user-detail", kwargs={"pk": user.pk})

        self.assertEqual(user.get_absolute_url(), expected_url)

    def test_default_login_attempts(self):
        user = User.objects.create_user(
            username="security_user",
            email="sec@test.com",
            password="pass",
        )
        self.assertEqual(user.login_attempts_count, 0)
        self.assertIsNone(user.block_timestamp)
