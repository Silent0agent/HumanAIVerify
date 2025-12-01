__all__ = ()

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
)

import users.forms

User = auth.get_user_model()


class ActivateUserView(View):
    template_name = "users/activation_success.html"

    def get(self, request, signed_username):
        signer = signing.TimestampSigner()

        try:
            username = signer.unsign(signed_username, max_age=3600 * 12)
            user = User.objects.get(username=username)
        except (signing.BadSignature, User.DoesNotExist):
            return HttpResponseNotFound(
                _("Invalid_or_expired_activation_link"),
            )

        user.is_active = True
        user.save()

        return render(request, self.template_name)


class SignUpView(FormView):
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        if not settings.DEFAULT_USER_IS_ACTIVE:
            self._send_activation_email(user)
            messages.warning(
                self.request,
                _("Need_to_activate_profile"),
            )
        else:
            messages.success(
                self.request,
                _("Succesfully_registred"),
            )

        return super().form_valid(form)

    def _send_activation_email(self, user):
        signer = signing.TimestampSigner()
        signed_username = signer.sign(user.username)
        activate_link = self.request.build_absolute_uri(
            reverse(
                "users:activate",
                kwargs={"signed_username": signed_username},
            ),
        )

        send_mail(
            subject=_("Profile_activation"),
            message=render_to_string(
                "users/subjects/activation_email.txt",
                {"activate_link": activate_link},
            ),
            from_email=settings.EMAIL_HOST,
            recipient_list=[user.email],
        )


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = users.forms.UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Settings_saved"))
        self.request.session.modified = True
        return super().form_valid(form)


class LoginView(LoginView):
    form_class = users.forms.CustomAuthenticationForm
    template_name = "users/login.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super().form_valid(form)


class LogoutView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        messages.info(request, _("Successful_logout"))
        return HttpResponseRedirect(reverse("users:login"))


class UnlockAccountView(View):
    template_name = "users/activation_success.html"

    def get(self, request, signed_username):
        signer = signing.TimestampSigner()

        try:
            username = signer.unsign(signed_username, max_age=3600 * 7)
            user = User.objects.get(username=username)
        except (signing.BadSignature, User.DoesNotExist):
            return HttpResponseNotFound(
                _("Invalid_or_expired_activation_link"),
            )

        user.is_active = True
        user.login_attempts_count = 0
        user.block_timestamp = None
        user.save()

        return render(request, self.template_name)


class UserDetailView(DetailView):
    context_object_name = "user"
    template_name = "users/user_detail.html"

    def get_queryset(self):
        return User.objects.public_information()


class UserListView(LoginRequiredMixin, ListView):
    context_object_name = "user_list"
    template_name = "users/user_list.html"

    def get_queryset(self):
        return User.objects.public_information()
