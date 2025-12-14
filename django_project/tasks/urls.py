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
        "user-text-tasks/",
        tasks.views.UserTextTasksListView.as_view(),
        name="user-text-tasks",
    ),
    path(
        "user-text-checks/",
        tasks.views.UserTextChecksListView.as_view(),
        name="user-text-checks",
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
        "user-image-tasks/",
        tasks.views.UserImageTasksListView.as_view(),
        name="user-image-tasks",
    ),
    path(
        "user-image-checks/",
        tasks.views.UserImageChecksListView.as_view(),
        name="user-image-checks",
    ),
]
