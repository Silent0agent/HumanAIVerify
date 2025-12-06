__all__ = ()
from django.urls import path

import tasks.views

app_name = "tasks"

urlpatterns = [
    path("create/", tasks.views.TextTaskCreateView.as_view(), name="create"),
    path(
        "<int:task_id>/check/",
        tasks.views.TaskCheckPerformView.as_view(),
        name="check",
    ),
]
