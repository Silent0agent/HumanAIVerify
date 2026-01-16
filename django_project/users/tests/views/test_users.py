__all__ = ()

from http import HTTPStatus

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

User = auth.get_user_model()


class UsersViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword",
            is_active=True,
            role=User.Role.CUSTOMER,
        )

    def setUp(self):
        self.user.role = User.Role.CUSTOMER
        self.user.save()
        self.client.force_login(self.user)

    def test_set_role_view_status_code_found(self):
        response = self.client.post(
            reverse("users:set-role"),
            {"role": User.Role.PERFORMER},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_set_role_view_redirects_to_homepage(self):
        response = self.client.post(
            reverse("users:set-role"),
            {"role": User.Role.PERFORMER},
        )

        self.assertRedirects(response, reverse("homepage:index"))

    def test_set_role_view_changes_role(self):
        self.client.post(
            reverse("users:set-role"),
            {"role": User.Role.PERFORMER},
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Role.PERFORMER)

    def test_user_detail_view_status_code_ok(self):
        response = self.client.get(
            reverse(
                "users:user-detail",
                kwargs={"pk": self.user.id},
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_detail_view_template(self):
        response = self.client.get(
            reverse(
                "users:user-detail",
                kwargs={"pk": self.user.id},
            ),
        )
        self.assertTemplateUsed(response, "users/user_detail.html")

    def test_user_detail_user_object_in_context(self):
        response = self.client.get(
            reverse(
                "users:user-detail",
                kwargs={"pk": self.user.id},
            ),
        )
        self.assertIn("user_obj", response.context)

    def test_user_detail_only_public_fields_in_context(self):
        response = self.client.get(
            reverse(
                "users:user-detail",
                kwargs={"pk": self.user.id},
            ),
        )
        public_fields = {
            User.id.field.name,
            User.email.field.name,
            User.username.field.name,
            User.avatar.field.name,
            User.role.field.name,
            User.date_joined.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.last_login.field.name,
        }
        all_model_fields = {field.name for field in User._meta.get_fields()}
        private_fields = all_model_fields - public_fields

        user_context = response.context["user_obj"]

        for private_field in private_fields:
            with self.subTest(field=private_field):
                self.assertNotIn(
                    private_field,
                    user_context.__dict__,
                )

    def test_profile_view_status_code_ok(self):
        response = self.client.get(
            reverse(
                "users:profile",
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_view_template(self):
        response = self.client.get(
            reverse(
                "users:profile",
            ),
        )
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_context(self):
        response = self.client.get(
            reverse(
                "users:profile",
            ),
        )
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)
