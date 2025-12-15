from django.urls import path

import tasks.views

urlpatterns = [
    path(
        "<int:pk>/",
        tasks.views.TextTaskDetailView.as_view(),
        name="text-task-detail",
    ),
    path(
        "create/",
        tasks.views.TextTaskCreateView.as_view(),
        name="text-task-create",
    ),
    path(
        "<int:task_id>/check/",
        tasks.views.TextTaskCheckPerformView.as_view(),
        name="text-check-perform",
    ),
    path(
        "my/",
        tasks.views.UserTextTasksListView.as_view(),
        name="user-text-tasks",
    ),
    path(
        "my-checks/",
        tasks.views.UserTextChecksListView.as_view(),
        name="user-text-checks",
    ),
    path(
        "check/<int:check_id>/",
        tasks.views.TextTaskCheckDetailView.as_view(),
        name="text-check-detail",
    ),
]
