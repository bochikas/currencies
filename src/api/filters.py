from django_filters import rest_framework as filters

from rates.models import Rate


class RateFilter(filters.FilterSet):
    """Фильтр для курсов валют."""

    threshold = filters.NumberFilter(method='filter_threshold')
    date_from = filters.DateFilter(method='filter_date_from')
    date_to = filters.DateFilter(method='filter_date_to')

    class Meta:
        fields = ('threshold', 'date_from', 'date_to')
        model = Rate

    def filter_threshold(self, qs, name, value):
        return qs

    def filter_date_from(self, qs, name, value):
        if value:
            return qs.filter(date__gte=value)
        return qs

    def filter_date_to(self, qs, name, value):
        if value:
            return qs.filter(date__lte=value)
        return qs
