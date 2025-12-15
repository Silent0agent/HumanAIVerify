__all__ = ()

from django.contrib import auth
from django.test import TestCase

User = auth.get_user_model()


class BaseViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = User.objects.create_user(
            username="customer",
            email="example1@example.com",
            password="password",
            role=User.Role.CUSTOMER,
        )

        cls.performer = User.objects.create_user(
            username="performer",
            email="example2@example.com",
            password="password",
            role=User.Role.PERFORMER,
        )
