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
    template_name = 'training/start.html'
    progress_model = training.models.UserTrainingProgress
    text_model = training.models.TrainingText

    def get(self, request):
        try:
            progress = self.progress_model.objects.with_completed_texts_count().get(
                user=request.user,
            )
        except self.progress_model.DoesNotExist:
            progress = self.progress_model.objects.create(
                user=request.user,
            )
            progress.completed_texts_count = 0

        context_dict = {
            'progress': progress,
            'can_start': False,
            'needed_score': settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
        }

        if not progress.can_take_test:
            return render(request, self.template_name, context_dict)

        available_ids = list(
            progress.get_available_texts().values_list('id', flat=True),
        )

        if not available_ids:
            messages.info(request, _('No_more_training_texts_available'))
            return render(request, self.template_name, context_dict)

        random_id = random.choice(available_ids)

        return redirect('training:take-test', text_id=random_id)


class TrainingTakeTestView(LoginRequiredMixin, View):
    template_name = 'training/take_test.html'
    progress_model = training.models.UserTrainingProgress
    text_model = training.models.TrainingText

    def get(self, request, text_id):
        progress = get_object_or_404(
            self.progress_model.objects.with_text_completion_status(
                text_id,
            ),
            user=request.user,
        )

        if not progress.can_take_test:
            messages.error(request, _('You_need_to_wait'))
            return redirect('training:start')

        if progress.is_already_completed:
            messages.info(request, _('You_already_completed_this_text'))
            return redirect('training:start')

        training_text = get_object_or_404(
            self.text_model,
            id=text_id,
        )

        form = training.forms.TrainingTextForm(training_text=training_text)

        return render(
            request,
            self.template_name,
            {
                'training_text': training_text,
                'form': form,
                'progress': progress,
                'needed_score': settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )

    def post(self, request, text_id):
        progress = get_object_or_404(
            self.progress_model,
            user=request.user,
        )

        training_text = get_object_or_404(
            self.text_model,
            id=text_id,
        )
        form = training.forms.TrainingTextForm(
            request.POST,
            training_text=training_text,
        )

        if form.is_valid():
            user_answer = form.cleaned_data['is_ai_generated']
            is_correct = user_answer == training_text.is_ai_generated

            progress.add_completed_text(training_text, is_correct)

            if is_correct:
                messages.success(request, _('Correct_answer_plus_one_point'))
            else:
                messages.error(request, _('Wrong_answer_minus_two_points'))

            if progress.training_score >= settings.TRAINING_COMPLETIONS_FOR_PERFORMER:
                messages.success(
                    request,
                    _('You_are_now_a_performer'),
                )
                return redirect('training:results')

            return redirect('training:start')

        return render(
            request,
            self.template_name,
            {
                'training_text': training_text,
                'form': form,
                'progress': progress,
                'needed_score': settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )


class TrainingResultsView(LoginRequiredMixin, View):
    template_name = 'training/results.html'
    progress_model = training.models.UserTrainingProgress
    text_model = training.models.TrainingText

    def get(self, request):

        try:
            progress = self.progress_model.objects.with_completed_texts_count().get(
                user=request.user,
            )
        except self.progress_model.DoesNotExist:
            progress = self.progress_model.objects.create(
                user=request.user,
            )
            progress.completed_texts_count = 0

        return render(
            request,
            self.template_name,
            {
                'progress': progress,
                'completed_count': progress.completed_texts_count,
                'total_texts': self.text_model.objects.count(),
                'needed_score': settings.TRAINING_COMPLETIONS_FOR_PERFORMER,
            },
        )
