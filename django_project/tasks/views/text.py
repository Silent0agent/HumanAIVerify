__all__ = ()

import tasks.forms
import tasks.models
from tasks.views.base import (
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
    BaseUserChecksListView,
    BaseUserTasksListView,
)


class TextTaskCreateView(BaseTaskCreateView):
    model = tasks.models.TextTask
    form_class = tasks.forms.TextTaskForm


class TextTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    form_class = tasks.forms.TextTaskCheckForm
    template_name = "tasks/text/check_perform.html"


class UserTextTasksListView(BaseUserTasksListView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = "tasks/text/user_tasks.html"


class UserTextChecksListView(BaseUserChecksListView):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    template_name = "tasks/text/user_checks.html"


class TextTaskDetailView(BaseTaskDetailView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = "tasks/text/task_detail.html"
