__all__ = (
    "BaseTaskCreateView",
    "BaseTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskCheckPerformView",
)

from tasks.views.base import BaseTaskCheckPerformView, BaseTaskCreateView
from tasks.views.text import TextTaskCheckPerformView, TextTaskCreateView
