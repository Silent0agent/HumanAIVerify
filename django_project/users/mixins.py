__all__ = ()

from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

User = auth.get_user_model()


class RoleRequiredMixin(UserPassesTestMixin):
    def get_allowed_roles(self):
        return []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.request.user.role in self.get_allowed_roles()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(
            self.request,
            _("User_have_wrong_role"),
        )

        return redirect("homepage:index")


class CustomerRequiredMixin(RoleRequiredMixin):
    def get_allowed_roles(self):
        return [User.Role.CUSTOMER]


class PerformerRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated
            and user.groups.filter(name="Performers").exists()
        )

    def handle_no_permission(self):
        from django.contrib.auth.models import Group
        from training.models import UserTrainingProgress

        if self.request.user.is_authenticated:
            try:
                progress = UserTrainingProgress.objects.get(
                    user=self.request.user,
                )
                if progress.training_score >= 10:
                    performer_group, created = Group.objects.get_or_create(
                        name="Performers",
                    )
                    self.request.user.groups.add(performer_group)
                    messages.success(
                        self.request,
                        _("Congratulations_you_have_been_added_to_performers"),
                    )
                    return redirect(self.request.path)

                messages.warning(
                    self.request,
                    _("You_need_points_to_become_performer"),
                )
            except UserTrainingProgress.DoesNotExist:
                messages.info(
                    self.request,
                    _("Complete_training_to_become_performer"),
                )

            return redirect("training:start")

        return super().handle_no_permission()