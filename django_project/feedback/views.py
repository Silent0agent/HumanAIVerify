__all__ = ()

import threading

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

import core.utils
import feedback.forms
import feedback.models


class FeedbackView(TemplateView):
    template_name = 'feedback/feedback.html'
    success_url = reverse_lazy('feedback:feedback')

    def get_forms_dict(self):
        if self.request.method == 'POST':
            data = self.request.POST
            files = self.request.FILES
        else:
            data = None
            files = None

        return {
            'author_form': feedback.forms.FeedbackUserProfileForm(
                data,
                prefix='author',
            ),
            'content_form': feedback.forms.FeedbackForm(
                data,
                prefix='content',
            ),
            'files_form': feedback.forms.FeedbackFileForm(
                data,
                files,
                prefix='files',
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_forms_dict())
        return context

    def post(self, request, *args, **kwargs):
        forms = self.get_forms_dict()

        author_form = forms['author_form']
        content_form = forms['content_form']
        files_form = forms['files_form']

        if all(form.is_valid() for form in forms.values()):
            mail = author_form.cleaned_data['mail']
            name = author_form.cleaned_data['name']
            text = content_form.cleaned_data['text']

            author_profile, created = (
                feedback.models.FeedbackUserProfile.objects.update_or_create(
                    mail=mail,
                    defaults={'name': name},
                )
            )

            feedback_item = content_form.save(commit=False)
            feedback_item.author = author_profile
            feedback_item.save()

            files_form.save(feedback_instance=feedback_item)

            send_mail(
                _('Feedback_mail_head'),
                text,
                settings.EMAIL_FROM_DEFAULT,
                [mail],
                fail_silently=False,
            )
            threading.Thread(target=core.utils.send_mail_async).start()

            messages.success(request, _('Success_feedback_form'))
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {
                'author_form': author_form,
                'content_form': content_form,
                'files_form': files_form,
            },
        )
