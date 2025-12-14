__all__ = (
    "BaseUserChecksListView",
    "BaseUserTasksListView",
    "BaseTaskCheckPerformView",
    "BaseTaskCreateView",
    "BaseTaskDetailView",
    "UserTextChecksListView",
    "UserTextTasksListView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
    "UserImageChecksListView",
    "UserImageTasksListView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
)

from tasks.views.base import (
    BaseTaskCheckPerformView,
    BaseTaskCreateView,
    BaseTaskDetailView,
    BaseUserChecksListView,
    BaseUserTasksListView,
)
from tasks.views.image import (
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    UserImageChecksListView,
    UserImageTasksListView,
)
from tasks.views.text import (
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
    UserTextChecksListView,
    UserTextTasksListView,
)
