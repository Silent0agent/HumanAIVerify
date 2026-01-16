__all__ = ()

from django.db import models


class TrainingProgressQuerySet(models.QuerySet):
    def with_completed_texts_count(self):
        completed_texts = self.model.completed_texts.field.name
        return self.annotate(
            completed_texts_count=models.Count(
                completed_texts,
            ),
        )

    def with_text_completion_status(self, text_id):
        completed_texts_field = self.model.completed_texts.field
        through_model = completed_texts_field.remote_field.through

        source_field = next(
            field
            for field in through_model._meta.get_fields()
            if field.is_relation and field.related_model == self.model
        )

        target_field = next(
            field
            for field in through_model._meta.get_fields()
            if field.is_relation
            and field.related_model == completed_texts_field.related_model
        )

        filter_kwargs = {
            source_field.name: models.OuterRef("pk"),
            target_field.name: text_id,
        }

        return self.annotate(
            is_already_completed=models.Exists(
                through_model.objects.filter(**filter_kwargs),
            ),
        )
