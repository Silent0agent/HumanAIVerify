__all__ = ()

import tasks.forms
import tasks.models
from tasks.views.base import BaseMyChecksListView, BaseMyTasksListView
from tasks.views.base import BaseTaskCheckPerformView, BaseTaskCreateView
from tasks.views.base import BaseTaskDetailView


class TextTaskCreateView(BaseTaskCreateView):
    model = tasks.models.TextTask
    form_class = tasks.forms.TextTaskForm


class TextTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    form_class = tasks.forms.TextTaskCheckForm
    template_name = "tasks/text_check_perform.html"


class MyTextTasksListView(BaseMyTasksListView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = "tasks/my_text_tasks.html"


class MyTextChecksListView(BaseMyChecksListView):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask


class TextTaskDetailView(BaseTaskDetailView):
    model = tasks.models.TextTask
    template_name = "tasks/my_text_checks.html"
