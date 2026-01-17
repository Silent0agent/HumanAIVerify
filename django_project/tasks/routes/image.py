from django.urls import path

import tasks.views

urlpatterns = [
    path(
        'my/',
        tasks.views.CustomerImageTasksListView.as_view(),
        name='my-image-tasks',
    ),
    path(
        'create/',
        tasks.views.ImageTaskCreateView.as_view(),
        name='image-task-create',
    ),
    path(
        '<int:task_id>/',
        tasks.views.ImageTaskDetailView.as_view(),
        name='image-task-detail',
    ),
    path(
        'my-checks/',
        tasks.views.PerformerImageChecksListView.as_view(),
        name='my-image-checks',
    ),
    path(
        'check/<int:check_id>/',
        tasks.views.ImageTaskCheckDetailView.as_view(),
        name='image-check-detail',
    ),
    path(
        '<int:task_id>/check/',
        tasks.views.ImageTaskCheckPerformView.as_view(),
        name='image-check-perform',
    ),
    path(
        'check/<int:check_id>/',
        tasks.views.ImageTaskCheckDetailView.as_view(),
        name='image-check-detail',
    ),
]
