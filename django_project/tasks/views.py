__all__ = ()

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from tasks.forms import TaskCheckForm, TextTaskForm
from tasks.models import TaskCheck, TextTask


class TextTaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TextTask
    form_class = TextTaskForm
    template_name = "tasks/texttask_create.html"

    def test_func(self):
        return self.request.user.role == "customer"

    def handle_no_permission(self):
        messages.error(self.request, _("Only_customers_can_create_tasks"))
        return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, _("Task_created_successfully"))
        return super().form_valid(form)


class TaskCheckCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TaskCheck
    form_class = TaskCheckForm
    template_name = "tasks/taskcheck_create.html"

    def test_func(self):
        return self.request.user.role == "performer"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(TextTask, pk=kwargs["task_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.task
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("Only_performers_can_check_tasks"))
        return super().handle_no_permission()

    def form_valid(self, form):
        if TaskCheck.objects.filter(
            task=self.task,
            performer=self.request.user,
        ).exists():
            messages.error(
                self.request,
                _("You_have_already_checked_this_task"),
            )
            return self.form_invalid(form)

        form.instance.performer = self.request.user
        form.instance.task = self.task
        messages.success(self.request, _("Task_check_submitted"))
        return super().form_valid(form)
