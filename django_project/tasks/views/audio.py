__all__ = ()

import tasks.forms
import tasks.models
from tasks.views.base import (
    BaseMyChecksListView,
    BaseMyTasksListView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
)


class AudioTaskCreateView(BaseTaskCreateView):
    model = tasks.models.AudioTask
    form_class = tasks.forms.AudioTaskForm


class AudioTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    form_class = tasks.forms.AudioTaskCheckForm
    template_name = "tasks/audio/audio_check_perform.html"


class MyAudioTasksListView(BaseMyTasksListView):
    model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    template_name = "tasks/audio/my_audio_tasks.html"


class MyAudioChecksListView(BaseMyChecksListView):
    model = tasks.models.AudioTaskCheck
    task_model = tasks.models.AudioTask
    template_name = "tasks/audio/my_audio_checks.html"


class AudioTaskDetailView(BaseTaskDetailView):
    model = tasks.models.AudioTask
    check_model = tasks.models.AudioTaskCheck
    template_name = "tasks/audio/audio_task_detail.html"
