__all__ = ()

import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

import training.forms
import training.models


class TrainingStartView(LoginRequiredMixin, View):
    template_name = "training/start.html"

    def get(self, request):
        progress, created = (
            training.models.UserTrainingProgress.objects.get_or_create(
                user=request.user,
            )
        )
        if request.user.groups.filter(name='Performers').exists():
            return redirect('training:results')
        context_dict = {
            "progress": progress,
            "can_start": False,
            "needed_score": settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
        }

        if not progress.can_take_test:
            messages.warning(
                request,
                _("Try_again_in_hours").format(
                    hours=progress.remaining_hours,
                ),
            )
            return render(
                request,
                self.template_name,
                context_dict,
            )

        available_texts = progress.get_available_texts()
        if not available_texts.exists():
            messages.info(request, _("No_more_training_texts_available"))
            return render(
                request,
                self.template_name,
                context_dict,
            )

        training_text = random.choice(list(available_texts))

        return redirect("training:take-test", text_id=training_text.id)


class TrainingTakeTestView(LoginRequiredMixin, View):
    template_name = "training/take_test.html"

    def get(self, request, text_id):
        progress = get_object_or_404(
            training.models.UserTrainingProgress,
            user=request.user,
        )

        if not progress.can_take_test:
            messages.error(request, _("You_need_to_wait"))
            return redirect("training:start")

        training_text = get_object_or_404(
            training.models.TrainingText,
            id=text_id,
        )

        if progress.completed_texts.filter(id=text_id).exists():
            messages.info(request, _("You_already_completed_this_text"))
            return redirect("training:start")

        form = training.forms.TrainingTextForm(training_text=training_text)

        return render(
            request,
            self.template_name,
            {
                "training_text": training_text,
                "form": form,
                "progress": progress,
                "needed_score": settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )

    def post(self, request, text_id):
        progress = get_object_or_404(
            training.models.UserTrainingProgress,
            user=request.user,
        )

        training_text = get_object_or_404(
            training.models.TrainingText,
            id=text_id,
        )
        form = training.forms.TrainingTextForm(
            request.POST,
            training_text=training_text,
        )

        if form.is_valid():
            user_answer = form.cleaned_data["is_ai_generated"]
            is_correct = user_answer == training_text.is_ai_generated

            progress.add_completed_text(training_text, is_correct)

            if is_correct:
                messages.success(request, _("Correct_answer_plus_1_point"))
            else:
                messages.error(request, _("Wrong_answer_minus_2_points"))

            if (
                progress.training_score
                >= settings.TRAINING_COMPLETIONS_FOR_PERFORMER
            ):
                messages.success(
                    request,
                    _("You_are_now_a_performer"),
                )
                return redirect("training:results")

            return redirect("training:start")

        return render(
            request,
            self.template_name,
            {
                "training_text": training_text,
                "form": form,
                "progress": progress,
                "needed_score": settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )


class TrainingResultsView(LoginRequiredMixin, View):
    template_name = "training/results.html"

    def get(self, request):
        progress, created = (
            training.models.UserTrainingProgress.objects.get_or_create(
                user=request.user,
            )
        )

        return render(
            request,
            self.template_name,
            {
                "progress": progress,
                "completed_count": progress.completed_texts.count(),
                "total_texts": training.models.TrainingText.objects.count(),
                "needed_score": settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )
