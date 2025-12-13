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
from tasks.views.base import BaseTaskCheckDetailView


class TextTaskCreateView(BaseTaskCreateView):
    model = tasks.models.TextTask
    form_class = tasks.forms.TextTaskForm


class TextTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    form_class = tasks.forms.TextTaskCheckForm
    template_name = "tasks/text/text_check_perform.html"

    def get(self, request, *args, **kwargs):
        if self.check_obj and self.check_obj.annotated_content:
            initial_annotated = self.check_obj.annotated_content
        else:
            initial_annotated = self.task.content

        return super().get(
            request,
            form_attrs={
                "initial": {
                    "content": self.task.content,
                    "highlighted_content": initial_annotated,
                },
            },
        )

    def post(self, request, *args, **kwargs):
        return super().post(
            request,
            check_fields={
                "annotated_content": request.POST.getlist(
                    "highlighted_content",
                )[0]
                or self.task.content,
            },
        )


class MyTextTasksListView(BaseMyTasksListView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = "tasks/text/my_text_tasks.html"


class MyTextChecksListView(BaseMyChecksListView):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    template_name = "tasks/text/my_text_checks.html"


class TextTaskDetailView(BaseTaskDetailView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = "tasks/text/text_task_detail.html"


class TextTaskCheckDetailView(BaseTaskCheckDetailView):
    model = tasks.models.TextTaskCheck
