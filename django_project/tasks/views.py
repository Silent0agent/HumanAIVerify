__all__ = ()

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, View

import tasks.forms
import tasks.models
import users.mixins


class TextTaskCreateView(
    LoginRequiredMixin,
    users.mixins.CustomerRequiredMixin,
    CreateView,
):
    model = tasks.models.TextTask
    form_class = tasks.forms.TextTaskForm
    template_name = "tasks/texttask_create.html"
    success_url = reverse_lazy("homepage:index")

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, _("Task_created_successfully"))
        return super().form_valid(form)


class TaskCheckPerformView(
    LoginRequiredMixin,
    users.mixins.PerformerRequiredMixin,
    View,
):
    template_name = "tasks/taskcheck_create.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(
            tasks.models.TextTask,
            pk=kwargs["task_id"],
        )
        self.check_obj = tasks.models.TaskCheck.objects.filter(
            task=self.task,
            performer=request.user,
        ).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = tasks.forms.TaskCheckForm(instance=self.check_obj)
        return render(
            request,
            self.template_name,
            {"form": form, "task": self.task},
        )

    def post(self, request, *args, **kwargs):
        form = tasks.forms.TaskCheckForm(request.POST, instance=self.check_obj)

        if form.is_valid():
            check = form.save(commit=False)
            check.task = self.task
            check.performer = request.user
            action = request.POST.get("action")

            if action == "publish":
                check.status = tasks.models.TaskCheck.Status.PUBLISHED
                message = _("Check_published")
            else:
                check.status = tasks.models.TaskCheck.Status.DRAFT
                message = _("Draft_saved")

            check.save()
            messages.success(request, message)

            if check.status == tasks.models.TaskCheck.Status.PUBLISHED:
                return redirect("homepage:index")

            return redirect(request.path)

        return render(
            request,
            self.template_name,
            {"form": form, "task": self.task},
        )
