from django.urls import path

from .views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventResultListView,
    EventUpdateView,
    RaceCreateView,
    RaceResultCreateView,
    RaceResultsImportView,
    RaceSeriesCreateView,
    RaceSeriesDetailView,
    RaceSeriesUpdateView,
    EventsWaitingApproval,
)

app_name = "event"

urlpatterns = [
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/<int:pk>/update/", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("events/upload_results/<int:event_pk>", RaceResultsImportView, name="import_race_results"),
    path("events/results/", EventResultListView.as_view(), name="events_results_list"),
    path("raceseries/<int:pk>", RaceSeriesDetailView.as_view(), name="raceseries_detail"),
    path("raceseries/create/", RaceSeriesCreateView.as_view(), name="raceseries_create"),
    path("raceseries/<int:pk>/update/", RaceSeriesUpdateView.as_view(), name="raceseries_update"),
    path("race/create/", RaceCreateView.as_view(), name="race_create"),
    path("raceresult/create/", RaceResultCreateView.as_view(), name="raceresult_create"),
    path("events/approval/", EventsWaitingApproval.as_view(), name="events_waiting_approval"),
]
