__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from multi_form_view import MultiFormView

import feedback.forms
import feedback.models


class FeedbackView(MultiFormView):
    template_name = "feedback/feedback.html"
    form_classes = {
        "author_form": feedback.forms.FeedbackUserProfileForm,
        "content_form": feedback.forms.FeedbackForm,
        "files_form": feedback.forms.FeedbackFileForm,
    }
    success_url = reverse_lazy("feedback:feedback")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_form"] = self.forms["author_form"]
        context["content_form"] = self.forms["content_form"]
        context["files_form"] = self.forms["files_form"]
        return context

    def get_forms(self, **kwargs):
        author_form = feedback.forms.FeedbackUserProfileForm(
            self.request.POST or None,
        )
        content_form = feedback.forms.FeedbackForm(self.request.POST or None)
        files_form = feedback.forms.FeedbackFileForm(
            self.request.POST or None,
            self.request.FILES or None,
        )

        self.forms = {
            "author_form": author_form,
            "content_form": content_form,
            "files_form": files_form,
        }
        return self.forms

    def forms_valid(self, forms):
        mail = forms["author_form"].cleaned_data["mail"]
        name = forms["author_form"].cleaned_data["name"]
        text = forms["content_form"].cleaned_data["text"]
        author_profile, created = (
            feedback.models.FeedbackUserProfile.objects.update_or_create(
                mail=mail,
                defaults={"name": name},
            )
        )
        feedback_item = forms["content_form"].save(commit=False)
        feedback_item.author = author_profile
        feedback_item.save()
        forms["files_form"].save(feedback_instance=feedback_item)
        send_mail(
            _("feedback_mail_head"),
            text,
            settings.DEFAULT_FROM_EMAIL,
            [mail],
            fail_silently=False,
        )
        messages.success(self.request, _("success_feedback_form"))

        return super().forms_valid(forms)
