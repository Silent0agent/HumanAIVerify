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
        tasks.views.MyImageTasksListView.as_view(),
        name="my-image-tasks",
    ),
    path(
        "my-checks/",
        tasks.views.MyImageChecksListView.as_view(),
        name="my-image-checks",
    ),
]
