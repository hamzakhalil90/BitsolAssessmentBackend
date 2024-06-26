from rest_framework.pagination import LimitOffsetPagination
from apps.baselayer.utils import get_query_param


class CustomPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return list(), self.count
        return list(queryset[self.offset:self.offset + self.limit]), self.count


def paginate_data(data, request):
    limit = get_query_param(request, 'limit', None)
    offset = get_query_param(request, 'offset', None)
    if limit and offset:
        pagination = CustomPagination()
        data, count = pagination.paginate_queryset(data, request)
        return data, count
    else:
        return data, data.count()
