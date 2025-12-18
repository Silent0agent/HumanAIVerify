__all__ = ()

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from training.models import UserTrainingProgress

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
            _("User_have_wrong_role"),
        )

        return redirect("homepage:index")


class CustomerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.Role.CUSTOMER]


class PerformerRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated
            and user.groups.filter(name=settings.PERFORMER_GROUP_NAME).exists()
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:

            try:
                progress = UserTrainingProgress.objects.get(
                    user=self.request.user,
                )
                if (
                    progress.training_score
                    >= settings.TRAINING_COMPLETIONS_FOR_PERFORMER
                ):
                    performer_group, created = Group.objects.get_or_create(
                        name=settings.PERFORMER_GROUP_NAME,
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
