from django.urls import path

import tasks.views

urlpatterns = [
    path(
        "my/",
        tasks.views.MyTextTasksListView.as_view(),
        name="my-text-tasks",
    ),
    path(
        "create/",
        tasks.views.TextTaskCreateView.as_view(),
        name="text-task-create",
    ),
    path(
        "<int:task_id>/",
        tasks.views.TextTaskDetailView.as_view(),
        name="text-task-detail",
    ),
    path(
        "my-checks/",
        tasks.views.MyTextChecksListView.as_view(),
        name="my-text-checks",
    ),
    path(
        "<int:task_id>/check/",
        tasks.views.TextTaskCheckPerformView.as_view(),
        name="text-check-perform",
    ),
    path(
        "check/<int:check_id>/",
        tasks.views.TextTaskCheckDetailView.as_view(),
        name="text-check-detail",
    ),
]
