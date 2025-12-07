__all__ = ()

from django.urls import path

import users.views

app_name = "users"

urlpatterns = [
    path(
        "profile/",
        users.views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "user-detail/<int:pk>/",
        users.views.UserDetailView.as_view(),
        name="user-detail",
    ),
    path("set-role/", users.views.SetRoleView.as_view(), name="set-role"),
]
