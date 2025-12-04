__all__ = ()

from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "user-detail/<int:pk>",
        views.UserDetailView.as_view(),
        name="user-detail",
    ),
]
