__all__ = ()

from django.urls import path

import tasks.views

app_name = "tasks"

urlpatterns = [
    path(
        "text-task/create/",
        tasks.views.TextTaskCreateView.as_view(),
        name="text-task-create",
    ),
    path(
        "text-task/<int:task_id>/check/",
        tasks.views.TextTaskCheckPerformView.as_view(),
        name="text-check-perform",
    ),
    path(
        "my-text-tasks/",
        tasks.views.MyTextTasksListView.as_view(),
        name="my-text-tasks",
    ),
    path(
        "my-text-checks/",
        tasks.views.MyTextChecksListView.as_view(),
        name="my-text-checks",
    ),
]
