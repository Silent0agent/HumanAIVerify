__all__ = ()

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import Group
from django.test import TestCase

User = auth.get_user_model()


class BaseViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.performer_group, _ = Group.objects.get_or_create(
            name=settings.PERFORMER_GROUP_NAME,
        )
        cls.customer = User.objects.create_user(
            username='customer',
            email='example1@example.com',
            password='password',
            role=User.Role.CUSTOMER,
        )

        cls.performer = User.objects.create_user(
            username='performer',
            email='example2@example.com',
            password='password',
            role=User.Role.PERFORMER,
        )
        cls.performer.groups.add(cls.performer_group)
