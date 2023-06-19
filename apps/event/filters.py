from datetime import date

import django_filters
from django_filters import Filter

from .models import Event


class PastFilter(Filter):
    def filter(self, qs, value):
        if value is not None:
            if value:
                return qs.filter(end_date__lte=date.today()).order_by("-start_date")
            else:
                return qs.filter(end_date__gte=date.today())
        return qs


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    website = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.CharFilter(lookup_expr="icontains")
    is_usac_permitted = django_filters.BooleanFilter()
    featured_event = django_filters.BooleanFilter()
    past_events = PastFilter()

    class Meta:
        model = Event
        fields = ["name", "website", "city", "state", "is_usac_permitted", "featured_event", "past_events"]
