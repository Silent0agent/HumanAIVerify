__all__ = (
    "AudioTaskCheckDetailView",
    "AudioTaskCheckPerformView",
    "AudioTaskCreateView",
    "AudioTaskDetailView",
    "MyAudioChecksListView",
    "MyAudioTasksListView",
    "ImageTaskCheckDetailView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
    "MyImageChecksListView",
    "MyImageTasksListView",
    "TextTaskCheckDetailView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
    "MyTextChecksListView",
    "MyTextTasksListView",
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
