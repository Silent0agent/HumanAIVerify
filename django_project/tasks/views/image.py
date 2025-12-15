__all__ = ()

import tasks.forms
import tasks.models
from tasks.views.base import (
    BaseTaskCheckDetailView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
    BaseUserChecksListView,
    BaseUserTasksListView,
)


class ImageTaskCreateView(BaseTaskCreateView):
    model = tasks.models.ImageTask
    form_class = tasks.forms.ImageTaskForm


class ImageTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    form_class = tasks.forms.ImageTaskCheckForm
    template_name = "tasks/image/check_perform.html"


class UserImageTasksListView(BaseUserTasksListView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = "tasks/image/user_tasks.html"


class UserImageChecksListView(BaseUserChecksListView):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    template_name = "tasks/image/user_checks.html"


class ImageTaskDetailView(BaseTaskDetailView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = "tasks/image/task_detail.html"


class ImageTaskCheckDetailView(BaseTaskCheckDetailView):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    template_name = "tasks/image/task_check_detail.html"
