__all__ = (
    "MyTextChecksListView",
    "MyTextTasksListView",
    "TextTaskCheckDetailView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
    "ImageTaskCheckDetailView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
    "MyImageChecksListView",
    "MyImageTasksListView",
    "AudioTaskCheckDetailView",
    "AudioTaskCheckPerformView",
    "AudioTaskCreateView",
    "AudioTaskDetailView",
    "MyAudioChecksListView",
    "MyAudioTasksListView",
)

from tasks.views.audio import (
    AudioTaskCheckDetailView,
    AudioTaskCheckPerformView,
    AudioTaskCreateView,
    AudioTaskDetailView,
    MyAudioChecksListView,
    MyAudioTasksListView,
)
from tasks.views.image import (
    ImageTaskCheckDetailView,
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    MyImageChecksListView,
    MyImageTasksListView,
)
from tasks.views.text import (
    MyTextChecksListView,
    MyTextTasksListView,
    TextTaskCheckDetailView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
)
