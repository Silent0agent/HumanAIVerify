__all__ = ()

from django.contrib.auth import views as django_views
from django.urls import path, reverse_lazy

import users.views


app_name = "auth"

urlpatterns = [
    path(
        "login/",
        users.views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        users.views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "signup/",
        users.views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "activate/<signed_username>/",
        users.views.ActivateUserView.as_view(),
        name="activate",
    ),
    path(
        "unlock-account/<signed_username>/",
        users.views.UnlockAccountView.as_view(),
        name="unlock-account",
    ),
    path(
        "change-password/",
        users.views.PasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "reset-password/",
        users.views.PasswordResetView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/done/",
        django_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password-reset-done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        django_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("auth:password-reset-complete"),
        ),
        name="password-reset-confirm",
    ),
    path(
        "reset-password/complete/",
        django_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password-reset-complete",
    ),
]
