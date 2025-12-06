__all__ = ()

from django.contrib import auth
from django.contrib.auth.mixins import UserPassesTestMixin

User = auth.get_user_model()


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        return super().handle_no_permission()


class CustomerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.Role.CUSTOMER]


class PerformerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.Role.PERFORMER]
