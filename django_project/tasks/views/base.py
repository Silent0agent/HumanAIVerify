__all__ = ()

from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

import users.mixins

User = auth.get_user_model()


class BaseTaskCreateView(
    LoginRequiredMixin,
    users.mixins.CustomerRequiredMixin,
    CreateView,
):
    model = None
    form_class = None
    success_url = reverse_lazy("homepage:index")
    template_name = "tasks/task_create.html"

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, _("Task_created_successfully"))
        return super().form_valid(form)


class BaseTaskCheckPerformView(
    LoginRequiredMixin,
    users.mixins.PerformerRequiredMixin,
    View,
):
    task_model = None
    check_model = None
    form_class = None
    template_name = None

    def dispatch(self, request, *args, **kwargs):
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


class BaseUserTasksListView(
    LoginRequiredMixin,
    users.mixins.CustomerRequiredMixin,
    ListView,
):
    model = None
    check_model = None
    context_object_name = "tasks"
    template_name = None

    def get_queryset(self):
        user = self.request.user

        return (
            self.model.objects.by_client(user)
            .with_avg_ai_score(self.check_model)
            .with_checks_count(self.check_model)
        )


class BaseUserChecksListView(
    LoginRequiredMixin,
    users.mixins.PerformerRequiredMixin,
    ListView,
):
    model = None
    task_model = None
    context_object_name = "checks"
    template_name = None

    def get_queryset(self):
        all_needed_models_qs = self.model.objects.with_task().with_task_client(
            self.task_model,
        )
        task_title = (
            f"{self.model.task.field.name}__"
            f"{self.task_model.title.field.name}"
        )
        task_client_username = (
            f"{self.model.task.field.name}__"
            f"{self.task_model.client.field.name}__{User.username.field.name}"
        )

        return all_needed_models_qs.by_performer(self.request.user).only(
            task_title,
            task_client_username,
            self.model.ai_score.field.name,
            self.model.status.field.name,
            self.model.updated_at.field.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_username = (
            f"{self.task_model.client.field.name}__{User.username.field.name}"
        )
        all_needed_models_qs = self.task_model.objects.with_client()

        context[
            "available_tasks"
        ] = all_needed_models_qs.available_for_performer(
            user=self.request.user,
            check_model=self.model,
        ).only(
            self.task_model.title.field.name,
            self.model.created_at.field.name,
            client_username,
        )

        return context


class BaseTaskDetailView(
    LoginRequiredMixin,
    users.mixins.CustomerRequiredMixin,
    DetailView,
):
    model = None
    check_model = None
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_checks_with_performers(self.check_model)
            .with_checks_count(self.check_model)
            .with_avg_ai_score(self.check_model)
        )

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.client_id != self.request.user.id:
            raise PermissionDenied(_("You_are_not_the_owner_of_this_task"))

        return task
