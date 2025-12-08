__all__ = ()

from django.db import models


class TaskCheckManager(models.Manager):
    def published(self):
        return self.filter(status=self.model.Status.PUBLISHED)

    def get_avg_ai_score(self):
        ai_score_field = self.model.ai_score.field.name
        avg_queryset = self.published().aggregate(
            avg_score=models.Avg(ai_score_field),
        )
        return avg_queryset["avg_score"] or 0.0
