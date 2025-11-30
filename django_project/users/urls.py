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
        "user-detail/<int:pk>",
        views.UserDetailView.as_view(),
        name="user-detail",
    ),
    path(
        "user-list/",
        views.UserListView.as_view(),
        name="user-list",
    ),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "change-password/",
        django_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:change-password-done"),
        ),
        name="change-password",
    ),
    path(
        "change-password/done/",
        django_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="change-password-done",
    ),
    path(
        "reset-password/",
        django_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/subjects/password_reset.txt",
            success_url=reverse_lazy("users:password-reset-done"),
        ),
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
