__all__ = (
    "BaseMyChecksListView",
    "BaseMyTasksListView",
    "BaseTaskCheckPerformView",
    "BaseTaskCreateView",
    "BaseTaskDetailView",
    "MyTextChecksListView",
    "MyTextTasksListView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
)

from tasks.views.base import (
    BaseMyChecksListView,
    BaseMyTasksListView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
)
from tasks.views.text import (
    MyTextChecksListView,
    MyTextTasksListView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
)
