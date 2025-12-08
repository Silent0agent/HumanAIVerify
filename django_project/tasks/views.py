__all__ = ()

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, View

import users.mixins


class BaseTaskCreateView(
    LoginRequiredMixin,
    users.mixins.CustomerRequiredMixin,
    CreateView,
):
    template_name = "tasks/task_create.html"
    model = None
    form_class = None
    success_url = reverse_lazy("homepage:index")

    def dispatch(self, request, *args, **kwargs):
        required_definitions = [
            self.template_name,
            self.model,
            self.form_class,
        ]
        if not all(required_definitions):
            raise ImproperlyConfigured(
                "BaseTaskCreateView_improperly_configured",
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, _("Task_created_successfully"))
        return super().form_valid(form)


class BaseTaskCheckPerformView(
    LoginRequiredMixin,
    users.mixins.PerformerRequiredMixin,
    View,
):
    template_name = None
    task_model = None
    check_model = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        required_definitions = [
            self.template_name,
            self.task_model,
            self.check_model,
            self.form_class,
        ]
        if not all(required_definitions):
            raise ImproperlyConfigured(
                "BaseTaskCheckPerformView_improperly_configured",
            )

        self.task = get_object_or_404(
            self.task_model,
            pk=kwargs["task_id"],
        )

        self.check_obj = self.check_model.objects.filter(
            task=self.task,
            performer=request.user,
        ).first()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.check_obj)

        return render(
            request,
            self.template_name,
            {"form": form, "task": self.task},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.check_obj)

        if form.is_valid():
            check = form.save(commit=False)
            check.task = self.task
            check.performer = request.user
            action = request.POST.get("action")

            if action == "publish":
                check.status = self.check_model.Status.PUBLISHED
                message = _("Check_published")
            else:
                check.status = self.check_model.Status.DRAFT
                message = _("Draft_saved")

            check.save()
            messages.success(request, message)

            if check.status == self.check_model.Status.PUBLISHED:
                return redirect("homepage:index")

            return redirect(request.path)

        return render(
            request,
            self.template_name,
            {"form": form, "task": self.task},
        )
