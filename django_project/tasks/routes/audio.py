from django.urls import path

import tasks.views

urlpatterns = [
    path(
        'my/',
        tasks.views.MyAudioTasksListView.as_view(),
        name='my-audio-tasks',
    ),
    path(
        'create/',
        tasks.views.AudioTaskCreateView.as_view(),
        name='audio-task-create',
    ),
    path(
        '<int:task_id>/',
        tasks.views.AudioTaskDetailView.as_view(),
        name='audio-task-detail',
    ),
    path(
        'my-checks/',
        tasks.views.MyAudioChecksListView.as_view(),
        name='my-audio-checks',
    ),
    path(
        'check/<int:check_id>/',
        tasks.views.AudioTaskCheckDetailView.as_view(),
        name='audio-check-detail',
    ),
    path(
        '<int:task_id>/check/',
        tasks.views.AudioTaskCheckPerformView.as_view(),
        name='audio-check-perform',
    ),
    path(
        'check/<int:check_id>/',
        tasks.views.AudioTaskCheckDetailView.as_view(),
        name='audio-check-detail',
    ),
]
