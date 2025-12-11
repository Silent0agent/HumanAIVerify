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
    "MyImageChecksListView",
    "MyImageTasksListView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
)

from tasks.views.base import (
    BaseMyChecksListView,
    BaseMyTasksListView,
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
)
from tasks.views.image import (
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    MyImageChecksListView,
    MyImageTasksListView,
)
from tasks.views.text import (
    MyTextChecksListView,
    MyTextTasksListView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
)
