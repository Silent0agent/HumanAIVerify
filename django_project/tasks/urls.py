__all__ = ()

from django.urls import path

import tasks.forms
import tasks.models
import tasks.views

app_name = "tasks"

urlpatterns = [
    path(
        "text-task/create/",
        tasks.views.BaseTaskCreateView.as_view(
            model=tasks.models.TextTask,
            form_class=tasks.forms.TextTaskForm,
        ),
        name="text-task-create",
    ),
    path(
        "text-task/<int:task_id>/check/",
        tasks.views.BaseTaskCheckPerformView.as_view(
            template_name="tasks/text_check_perform.html",
            task_model=tasks.models.TextTask,
            check_model=tasks.models.TextTaskCheck,
            form_class=tasks.forms.TextTaskCheckForm,
        ),
        name="text-check-perform",
    ),
]
