__all__ = ()

from django.db import models


class TaskQuerySet(models.QuerySet):
    def by_client(self, user):
        return self.filter(client=user)

    def with_client(self):
        return self.select_related(self.model.client.field.name)

    def with_avg_ai_score(self, check_model):
        task_qs = check_model.objects.filter(
            task=models.OuterRef("id"),
            status=check_model.Status.PUBLISHED,
        ).values("task")
        avg_ai_score_qs = task_qs.annotate(
            avg_score=models.Avg(check_model.ai_score.field.name),
        ).values("avg_score")

        return self.annotate(
            _avg_ai_score=models.Subquery(
                avg_ai_score_qs,
                output_field=models.FloatField(),
            ),
        )

    def prefetch_checks(self, check_model, queryset=None):
        task_fk_field = check_model.task.field
        checks_attr_name = task_fk_field.remote_field.get_accessor_name()

        if queryset is None:
            queryset = check_model.objects.published()

        return self.prefetch_related(
            models.Prefetch(
                checks_attr_name,
                queryset=queryset,
            ),
        )

    def prefetch_checks_with_performers(self, check_model):
        performer_field_name = check_model.performer.field.name

        qs_with_performers = check_model.objects.published().select_related(
            performer_field_name,
        )

        return self.prefetch_checks(check_model, queryset=qs_with_performers)

    def with_checks_count(self, check_model):
        task_fk_field = check_model.task.field
        checks_lookup_name = task_fk_field.related_query_name()

        status_field_name = check_model.status.field.name
        status_path = f"{checks_lookup_name}__{status_field_name}"
        published_status = check_model.Status.PUBLISHED

        return self.annotate(
            checks_count=models.Count(
                checks_lookup_name,
                filter=models.Q((status_path, published_status)),
            ),
        )

    def available_for_performer(self, user, check_model):
        completed_tasks_qs = check_model.objects.by_performer(
            user=user,
        ).values(check_model.task.field.name)

        return self.exclude(id__in=completed_tasks_qs)


class CheckQuerySet(models.QuerySet):
    def by_performer(self, user):
        return self.filter(performer=user)

    def with_performer(self):
        return self.select_related(self.model.performer.field.name)

    def with_task(self):
        return self.select_related(self.model.task.field.name)

    def with_task_client(self, task_model):
        return self.select_related(
            f"{self.model.task.field.name}__{task_model.client.field.name}",
        )

    def published(self):
        return self.filter(status=self.model.Status.PUBLISHED)


class TaskCheckManager(models.Manager.from_queryset(CheckQuerySet)):
    def get_avg_ai_score(self):
        ai_score_field = self.model.ai_score.field.name

        avg_queryset = self.published().aggregate(
            avg_score=models.Avg(ai_score_field),
        )
        return avg_queryset["avg_score"]
