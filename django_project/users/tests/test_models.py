__all__ = ()

from django.contrib import auth
from django.test import TestCase
from parameterized import parameterized

User = auth.get_user_model()


class EmailNormalizationTest(TestCase):
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
        user = User(email=email)
        user.save()
        self.assertEqual(user.email, expected_normalized_email)
