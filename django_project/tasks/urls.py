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
        "my-tasks/",
        tasks.views.MyTextTasksListView.as_view(),
        name="my-tasks",
    ),
    path(
        "my-checks/",
        tasks.views.MyTextChecksListView.as_view(),
        name="my-checks",
    ),
    path(
        "text-task/<int:pk>/",
        tasks.views.TextTaskDetailView.as_view(),
        name="text-task-detail",
    ),
]
