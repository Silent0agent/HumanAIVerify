__all__ = ()

from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


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

        messages.error(
            self.request,
            _("user_ot_have_role"),
        )

        return redirect("homepage:index")


class CustomerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.Role.CUSTOMER]


class PerformerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.Role.PERFORMER]
