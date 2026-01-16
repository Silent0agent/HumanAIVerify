__all__ = ()

import tasks.forms
import tasks.models
from tasks.views.base import (
    BaseMyChecksListView,
    BaseMyTasksListView,
    BaseTaskCheckDetailView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
)


class MyAudioTasksListView(BaseMyTasksListView):
    model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    template_name = 'tasks/audio/my_tasks.html'


class AudioTaskCreateView(BaseTaskCreateView):
    model = tasks.models.AudioTask
    form_class = tasks.forms.AudioTaskForm


class AudioTaskDetailView(BaseTaskDetailView):
    model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    template_name = 'tasks/audio/task_detail.html'


class MyAudioChecksListView(BaseMyChecksListView):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    template_name = 'tasks/audio/my_checks.html'


class AudioTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    form_class = tasks.forms.AudioTaskCheckForm
    template_name = 'tasks/audio/check_perform.html'


class AudioTaskCheckDetailView(BaseTaskCheckDetailView):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    template_name = 'tasks/audio/check_detail.html'
