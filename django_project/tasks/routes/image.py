from django.urls import path

import tasks.views

urlpatterns = [
    path(
        "<int:pk>/",
        tasks.views.ImageTaskDetailView.as_view(),
        name="image-task-detail",
    ),
    path(
        "create/",
        tasks.views.ImageTaskCreateView.as_view(),
        name="image-task-create",
    ),
    path(
        "<int:task_id>/check/",
        tasks.views.ImageTaskCheckPerformView.as_view(),
        name="image-check-perform",
    ),
    path(
        "my/",
        tasks.views.UserImageTasksListView.as_view(),
        name="user-image-tasks",
    ),
    path(
        "my-checks/",
        tasks.views.UserImageChecksListView.as_view(),
        name="user-image-checks",
    ),
]
