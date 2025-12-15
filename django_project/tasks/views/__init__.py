__all__ = (
    "AudioTaskCheckDetailView",
    "AudioTaskCheckPerformView",
    "AudioTaskCreateView",
    "AudioTaskDetailView",
    "UserAudioChecksListView",
    "UserAudioTasksListView",
    "UserImageChecksListView",
    "UserImageTasksListView",
    "UserTextChecksListView",
    "UserTextTasksListView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
    "ImageTaskCheckDetailView",
    "TextTaskCheckDetailView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
)

from tasks.views.audio import (
    AudioTaskCheckDetailView,
    AudioTaskCheckPerformView,
    AudioTaskCreateView,
    AudioTaskDetailView,
    UserAudioChecksListView,
    UserAudioTasksListView,
)
from tasks.views.image import (
    ImageTaskCheckDetailView,
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    UserImageChecksListView,
    UserImageTasksListView,
)
from tasks.views.text import (
    TextTaskCheckDetailView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
    UserTextChecksListView,
    UserTextTasksListView,
)
