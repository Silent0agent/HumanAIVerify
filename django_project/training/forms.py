__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _


class TrainingTextForm(forms.Form):
    is_ai_generated = forms.TypedChoiceField(
        choices=[
            (True, _("AI_generated")),
            (False, _("Human_written")),
        ],
        coerce=lambda x: str(x).lower() == "true",
        widget=forms.RadioSelect,
        label=_("Is_this_text_AI_generated?"),
    )

    def __init__(self, *args, **kwargs):
        self.training_text = kwargs.pop("training_text", None)
        super().__init__(*args, **kwargs)
