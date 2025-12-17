__all__ = ()

from django.urls import path

import training.views

app_name = "training"

urlpatterns = [
    path("start/", training.views.TrainingStartView.as_view(), name="start"),
    path(
        "take-test/<int:text_id>/",
        training.views.TrainingTakeTestView.as_view(),
        name="take-test",
    ),
    path(
        "results/",
        training.views.TrainingResultsView.as_view(),
        name="results",
    ),
]
