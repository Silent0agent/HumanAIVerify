__all__ = ()

from django.urls import include, path

app_name = "tasks"

urlpatterns = [
    path("text/", include("tasks.routes.text")),
    path("image/", include("tasks.routes.image")),
    path("audio/", include("tasks.routes.audio")),
]
