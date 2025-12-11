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


class ImageTaskCreateView(BaseTaskCreateView):
    model = tasks.models.ImageTask
    form_class = tasks.forms.ImageTaskForm


class ImageTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    form_class = tasks.forms.ImageTaskCheckForm
    template_name = "tasks/image/image_check_perform.html"


class MyImageTasksListView(BaseMyTasksListView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = "tasks/image/my_image_tasks.html"


class MyImageChecksListView(BaseMyChecksListView):
    model = tasks.models.ImageTaskCheck
    task_model = tasks.models.ImageTask
    template_name = "tasks/image/my_image_checks.html"


class ImageTaskDetailView(BaseTaskDetailView):
    model = tasks.models.ImageTask
    check_model = tasks.models.ImageTaskCheck
    template_name = "tasks/image/image_task_detail.html"
