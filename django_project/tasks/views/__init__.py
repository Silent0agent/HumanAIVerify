__all__ = (
    "UserTextChecksListView",
    "UserTextTasksListView",
    "TextTaskCheckDetailView",
    "TextTaskCheckPerformView",
    "TextTaskCreateView",
    "TextTaskDetailView",
    "UserImageChecksListView",
    "UserImageTasksListView",
    "ImageTaskCheckPerformView",
    "ImageTaskCreateView",
    "ImageTaskDetailView",
    "UserAudioChecksListView",
    "UserAudioTasksListView",
    "AudioTaskCheckPerformView",
    "AudioTaskCreateView",
    "AudioTaskDetailView",
)

from tasks.views.audio import (
    AudioTaskCheckPerformView,
    AudioTaskCreateView,
    AudioTaskDetailView,
    UserAudioChecksListView,
    UserAudioTasksListView,
)
from tasks.views.image import (
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    UserImageChecksListView,
    UserImageTasksListView,
)
from tasks.views.text import (
    UserTextChecksListView,
    UserTextTasksListView,
    TextTaskCheckDetailView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
    UserTextChecksListView,
    UserTextTasksListView,
)
