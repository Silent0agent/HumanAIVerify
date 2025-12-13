__all__ = (
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
    "MyAudioChecksListView",
    "MyAudioTasksListView",
    "AudioTaskCheckPerformView",
    "AudioTaskCreateView",
    "AudioTaskDetailView",
)

from tasks.views.audio import (
    AudioTaskCheckPerformView,
    AudioTaskCreateView,
    AudioTaskDetailView,
    MyAudioChecksListView,
    MyAudioTasksListView,
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
