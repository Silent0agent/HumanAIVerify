__all__ = ()

import core.utils
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


class MyTextTasksListView(BaseMyTasksListView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = 'tasks/text/my_tasks.html'


class TextTaskCreateView(BaseTaskCreateView):
    model = tasks.models.TextTask
    form_class = tasks.forms.TextTaskForm


class TextTaskDetailView(BaseTaskDetailView):
    model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    template_name = 'tasks/text/task_detail.html'


class MyTextChecksListView(BaseMyChecksListView):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    template_name = 'tasks/text/my_checks.html'


class TextTaskCheckPerformView(BaseTaskCheckPerformView):
    task_model = tasks.models.TextTask
    check_model = tasks.models.TextTaskCheck
    form_class = tasks.forms.TextTaskCheckForm
    template_name = 'tasks/text/check_perform.html'

    def get(self, request, *args, **kwargs):
        initial_content = self.task.content
        if self.check_obj and self.check_obj.annotated_content:
            initial_content = self.check_obj.annotated_content

        return super().get(
            request,
            form_attrs={
                'initial': {
                    'highlighted_content': initial_content,
                    'content': self.task.content,
                },
            },
        )

    def post(self, request, *args, **kwargs):
        raw_html = request.POST.getlist('highlighted_content')[0]

        if raw_html:
            final_content = core.utils.sanitize_html(raw_html)
        else:
            final_content = self.task.content

        return super().post(
            request,
            check_fields={
                'annotated_content': final_content,
            },
        )


class TextTaskCheckDetailView(BaseTaskCheckDetailView):
    model = tasks.models.TextTaskCheck
    task_model = tasks.models.TextTask
    template_name = 'tasks/text/check_detail.html'
