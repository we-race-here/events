from django.urls import path

from .views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventResultListView,
    EventUpdateView,
    ImportRaceResults,
)

app_name = "event"

urlpatterns = [
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/<int:pk>/update/", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("events/upload_results/<int:event_pk>", ImportRaceResults, name="import_race_results"),
    path("events/results/", EventResultListView.as_view(), name="events_results_list"),
]
