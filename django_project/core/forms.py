__all__ = ()

from django import forms


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            widget = field.field.widget
            current_classes = widget.attrs.get('class', '')

            if isinstance(widget, forms.CheckboxInput):
                if 'form-check-input' not in current_classes:
                    widget.attrs['class'] = (
                        current_classes + ' form-check-input'
                    ).strip()
            else:
                if 'form-control' not in current_classes:
                    widget.attrs['class'] = (current_classes + ' form-control').strip()

            if not widget.attrs.get('placeholder'):
                widget.attrs['placeholder'] = field.label
