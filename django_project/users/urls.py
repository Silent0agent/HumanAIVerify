__all__ = ()

from django.contrib.auth import views as django_views
from django.urls import path, reverse_lazy

from users import views


app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "signup/",
        views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "activate/<signed_username>/",
        views.ActivateUserView.as_view(),
        name="activate",
    ),
    path(
        "unlock-account/<signed_username>/",
        views.UnlockAccountView.as_view(),
        name="unlock-account",
    ),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "change-password/",
        views.PasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "reset-password/",
        views.PasswordResetView.as_view(),
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
            success_url=reverse_lazy("users:password-reset-complete"),
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
