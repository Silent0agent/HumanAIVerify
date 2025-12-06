__all__ = ()
from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("create/", views.TextTaskCreateView.as_view(), name="task-create"),
    path(
        "task/<int:task_id>/check/",
        views.TaskCheckCreateView.as_view(),
        name="task-check",
    ),
]
