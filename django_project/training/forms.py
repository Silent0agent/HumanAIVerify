__all__ = ()

from django import forms
from django.utils.translation import gettext_lazy as _

import training.models


class TrainingTextForm(forms.ModelForm):
    class Meta:
        model = training.models.TrainingText
        fields = (training.models.TrainingText.is_ai_generated.field.name,)

    def __init__(self, *args, **kwargs):
        self.training_text = kwargs.pop("training_text", None)
        super().__init__(*args, **kwargs)

        self.fields[
            training.models.TrainingText.is_ai_generated.field.name
        ] = forms.TypedChoiceField(
            choices=[
                (True, _("AI_generated")),
                (False, _("Human_written")),
            ],
            coerce=lambda x: str(x).lower() == "true",
            widget=forms.RadioSelect,
            label=_("Is_this_text_AI_generated?"),
        )
