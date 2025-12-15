from django.urls import path

import tasks.views

urlpatterns = [
    path(
        "<int:pk>/",
        tasks.views.AudioTaskDetailView.as_view(),
        name="audio-task-detail",
    ),
    path(
        "create/",
        tasks.views.AudioTaskCreateView.as_view(),
        name="audio-task-create",
    ),
    path(
        "<int:task_id>/check/",
        tasks.views.AudioTaskCheckPerformView.as_view(),
        name="audio-check-perform",
    ),
    path(
        "my/",
        tasks.views.UserAudioTasksListView.as_view(),
        name="user-audio-tasks",
    ),
    path(
        "my-checks/",
        tasks.views.UserAudioChecksListView.as_view(),
        name="user-audio-checks",
    ),
]
