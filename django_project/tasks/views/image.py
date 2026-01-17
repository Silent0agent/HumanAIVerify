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


class CustomerImageTasksListView(BaseMyTasksListView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = 'tasks/image/my_tasks.html'


class ImageTaskCreateView(BaseTaskCreateView):
    model = tasks.models.ImageTask
    form_class = tasks.forms.ImageTaskForm


class ImageTaskDetailView(BaseTaskDetailView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = 'tasks/image/task_detail.html'


class PerformerImageChecksListView(BaseMyChecksListView):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    template_name = 'tasks/image/my_checks.html'


class ImageTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    form_class = tasks.forms.ImageTaskCheckForm
    template_name = 'tasks/image/check_perform.html'


class ImageTaskCheckDetailView(BaseTaskCheckDetailView):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    template_name = 'tasks/image/check_detail.html'
