__all__ = ()

from django.db import models


class TaskQuerySet(models.QuerySet):
    def by_client(self, user):
        return self.filter(client=user)

    def with_avg_ai_score(self, check_model):
        task_fk_field = check_model.task.field
        checks_lookup_name = task_fk_field.related_query_name()

        ai_score_field_name = check_model.ai_score.field.name
        status_field_name = check_model.status.field.name

        ai_score_path = f"{checks_lookup_name}__{ai_score_field_name}"
        status_path = f"{checks_lookup_name}__{status_field_name}"

        published_status = check_model.Status.PUBLISHED

        return self.annotate(
            _avg_ai_score=models.Avg(
                ai_score_path,
                filter=models.Q((status_path, published_status)),
            ),
        )

    def prefetch_checks(self, check_model):
        task_fk_field = check_model.task.field
        checks_attr_name = task_fk_field.remote_field.get_accessor_name()

        return self.prefetch_related(
            models.Prefetch(
                checks_attr_name,
                queryset=check_model.objects.published(),
            ),
        )

    def available_for_performer(self, user, check_model):
        completed_tasks_qs = check_model.objects.filter(
            performer=user,
        ).values(check_model.task.field.name)

        return self.exclude(id__in=completed_tasks_qs)


class CheckQuerySet(models.QuerySet):
    def by_performer(self, user):
        return self.filter(performer=user)

    def with_task(self):
        return self.select_related(self.model.task.field.name)

    def published(self):
        return self.filter(status=self.model.Status.PUBLISHED)


class TaskCheckManager(models.Manager.from_queryset(CheckQuerySet)):
    def get_avg_ai_score(self):
        ai_score_field = self.model.ai_score.field.name

        avg_queryset = self.published().aggregate(
            avg_score=models.Avg(ai_score_field),
        )
        return avg_queryset["avg_score"]
