__all__ = (
    "MyTextChecksListView",
    "MyTextTasksListView",
    "TextTaskCheckDetailView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
    "UserImageChecksListView",
    "UserImageTasksListView",
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
    UserImageChecksListView,
    UserImageTasksListView,
)
from tasks.views.text import (
    MyTextChecksListView,
    MyTextTasksListView,
    TextTaskCheckDetailView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
    UserTextChecksListView,
    UserTextTasksListView,
)
