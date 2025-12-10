__all__ = (
    "BaseMyChecksListView",
    "BaseMyTasksListView",
    "BaseTaskCheckPerformView",
    "BaseTaskCreateView",
    "MyTextChecksListView",
    "MyTextTasksListView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
)

from tasks.views.base import (
    BaseMyChecksListView,
    BaseMyTasksListView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
)
from tasks.views.text import (
    MyTextChecksListView,
    MyTextTasksListView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
)
