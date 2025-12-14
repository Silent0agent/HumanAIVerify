__all__ = ()

import core.utils
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
        initial_content = self.task.content
        if self.check_obj and self.check_obj.annotated_content:
            initial_content = self.check_obj.annotated_content

        return super().get(
            request,
            form_attrs={
                "initial": {
                    "highlighted_content": initial_content,
                    "content": self.task.content,
                },
            },
        )

    def post(self, request, *args, **kwargs):
        raw_html = request.POST.get("highlighted_content")

        if raw_html:
            final_content = core.utils.sanitize_html(raw_html)
        else:
            final_content = self.task.content

        return super().post(
            request,
            check_fields={
                "annotated_content": final_content,
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
    task_model = tasks.models.TextTask
    template_name = "tasks/text/task_check_detail.html"
