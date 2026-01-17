__all__ = (
    'AudioTaskCheckDetailView',
    'AudioTaskCheckPerformView',
    'AudioTaskCreateView',
    'AudioTaskDetailView',
    'PerformerAudioChecksListView',
    'CustomerAudioTasksListView',
    'ImageTaskCheckDetailView',
    'ImageTaskCheckPerformView',
    'ImageTaskCreateView',
    'ImageTaskDetailView',
    'PerformerImageChecksListView',
    'CustomerImageTasksListView',
    'TextTaskCheckDetailView',
    'TextTaskCheckPerformView',
    'TextTaskCreateView',
    'TextTaskDetailView',
    'PerformerTextChecksListView',
    'CustomerTextTasksListView',
)

from tasks.views.audio import (
    AudioTaskCheckDetailView,
    AudioTaskCheckPerformView,
    AudioTaskCreateView,
    AudioTaskDetailView,
    CustomerAudioTasksListView,
    PerformerAudioChecksListView,
)
from tasks.views.image import (
    CustomerImageTasksListView,
    ImageTaskCheckDetailView,
    ImageTaskCheckPerformView,
    ImageTaskCreateView,
    ImageTaskDetailView,
    PerformerImageChecksListView,
)
from tasks.views.text import (
    CustomerTextTasksListView,
    PerformerTextChecksListView,
    TextTaskCheckDetailView,
    TextTaskCheckPerformView,
    TextTaskCreateView,
    TextTaskDetailView,
)
