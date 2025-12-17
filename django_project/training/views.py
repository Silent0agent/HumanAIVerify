__all__ = ()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone

from .models import TrainingText, UserTrainingProgress
from .forms import TrainingTextForm


class TrainingStartView(LoginRequiredMixin, View):

    template_name = "training/start.html"

    def get(self, request):
        progress, created = UserTrainingProgress.objects.get_or_create(
            user=request.user
        )

        if not progress.can_take_test:
            messages.warning(
                request,
                _("You_can_try_again_in_hours").format(hours=progress.remaining_hours)
            )
            return render(request, self.template_name, {
                'progress': progress,
                'can_start': False,
            })

        available_texts = progress.get_available_texts()
        if not available_texts.exists():
            messages.info(request, _("No_more_training_texts_available"))
            return render(request, self.template_name, {
                'progress': progress,
                'can_start': False,
            })

        import random
        training_text = random.choice(list(available_texts))

        return redirect('training:take-test', text_id=training_text.id)


class TrainingTakeTestView(LoginRequiredMixin, View):

    template_name = "training/take_test.html"

    def get(self, request, text_id):
        progress = get_object_or_404(
            UserTrainingProgress,
            user=request.user
        )

        if not progress.can_take_test:
            messages.error(request, _("You_need_to_wait"))
            return redirect('training:start')

        training_text = get_object_or_404(TrainingText, id=text_id)

        if progress.completed_texts.filter(id=text_id).exists():
            messages.info(request, _("You_already_completed_this_text"))
            return redirect('training:start')

        form = TrainingTextForm(training_text=training_text)

        return render(request, self.template_name, {
            'training_text': training_text,
            'form': form,
            'progress': progress,
        })

    def post(self, request, text_id):
        progress = get_object_or_404(
            UserTrainingProgress,
            user=request.user
        )

        training_text = get_object_or_404(TrainingText, id=text_id)
        form = TrainingTextForm(request.POST, training_text=training_text)

        if form.is_valid():
            user_answer = form.cleaned_data['is_ai_generated']
            is_correct = (user_answer == training_text.is_ai_generated)

            progress.add_completed_text(training_text, is_correct)

            if is_correct:
                messages.success(request, _("Correct_answer_plus_1_point"))
            else:
                messages.error(request, _("Wrong_answer_minus_2_points"))

            if progress.training_score >= 10:
                messages.success(request, _("Congratulations_you_are_now_a_performer"))
                return redirect('training:results')

            return redirect('training:start')

        return render(request, self.template_name, {
            'training_text': training_text,
            'form': form,
            'progress': progress,
        })


class TrainingResultsView(LoginRequiredMixin, View):

    template_name = "training/results.html"

    def get(self, request):
        progress, created = UserTrainingProgress.objects.get_or_create(
            user=request.user
        )

        return render(request, self.template_name, {
            'progress': progress,
            'completed_count': progress.completed_texts.count(),
            'total_texts': TrainingText.objects.count(),
            'needed_score': 10,
        })
