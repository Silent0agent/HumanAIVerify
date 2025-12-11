__all__ = ()

from django.urls import path

import tasks.views

app_name = "tasks"

urlpatterns = [
    path(
        "text-task/<int:pk>/",
        tasks.views.TextTaskDetailView.as_view(),
        name="text-task-detail",
    ),
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
    path(
        "image-task/<int:pk>/",
        tasks.views.ImageTaskDetailView.as_view(),
        name="image-task-detail",
    ),
    path(
        "image-task/create/",
        tasks.views.ImageTaskCreateView.as_view(),
        name="image-task-create",
    ),
    path(
        "image-task/<int:task_id>/check/",
        tasks.views.ImageTaskCheckPerformView.as_view(),
        name="image-check-perform",
    ),
    path(
        "my-image-tasks/",
        tasks.views.MyImageTasksListView.as_view(),
        name="my-image-tasks",
    ),
    path(
        "my-image-checks/",
        tasks.views.MyImageChecksListView.as_view(),
        name="my-image-checks",
    ),
]
