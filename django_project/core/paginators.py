__all__ = ()

from django.core.paginator import Paginator
from django.utils.functional import cached_property


class CountOptimizedPaginator(Paginator):
    @cached_property
    def count(self):
        count_query = self.object_list.all()
        count_query.query.clear_ordering(force=True)
        count_query.query.select_related = False
        return count_query.values('pk').count()
