__all__ = ()

from django import forms


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            widget = field.field.widget

            widget.attrs.update(
                {
                    "placeholder": field.label,
                    "class": "form-control",
                },
            )

            if isinstance(field.field.widget, forms.CheckboxInput):
                widget.attrs.update(
                    {
                        "class": "form-check-input",
                    },
                )
