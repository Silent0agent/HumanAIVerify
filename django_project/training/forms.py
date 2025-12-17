__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _


class TrainingTextForm(forms.Form):

    is_ai_generated = forms.ChoiceField(
        choices=[
            (True, _("AI_generated")),
            (False, _("Human_written")),
        ],
        widget=forms.RadioSelect,
        label=_("Is_this_text_AI_generated?"),
    )

    def __init__(self, *args, **kwargs):
        self.training_text = kwargs.pop("training_text", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_ai_generated = cleaned_data.get("is_ai_generated")

        if is_ai_generated is not None:
            cleaned_data["is_ai_generated"] = is_ai_generated == "True"

        return cleaned_data
