__all__ = ()

from django.urls import path
from training import views

app_name = "training"

urlpatterns = [
    path("start/", views.TrainingStartView.as_view(), name="start"),
    path(
        "take-test/<int:text_id>/",
        views.TrainingTakeTestView.as_view(),
        name="take-test",
    ),
    path("results/", views.TrainingResultsView.as_view(), name="results"),
]
