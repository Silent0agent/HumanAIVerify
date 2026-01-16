__all__ = (
    'TextTaskForm',
    'TextTaskCheckForm',
    'ImageTaskForm',
    'ImageTaskCheckForm',
    'AudioTaskForm',
    'AudioTaskCheckForm',
)

from tasks.forms.audio import AudioTaskCheckForm, AudioTaskForm
from tasks.forms.image import ImageTaskCheckForm, ImageTaskForm
from tasks.forms.text import TextTaskCheckForm, TextTaskForm
