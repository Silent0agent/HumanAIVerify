__all__ = (
    "BaseTaskForm",
    "BaseTaskCheckForm",
    "TextTaskForm",
    "TextTaskCheckForm",
    "ImageTaskForm",
    "ImageTaskCheckForm",
)

from tasks.forms.base import BaseTaskCheckForm, BaseTaskForm
from tasks.forms.image import ImageTaskCheckForm, ImageTaskForm
from tasks.forms.text import TextTaskCheckForm, TextTaskForm
