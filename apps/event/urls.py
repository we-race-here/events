from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
)


app_name = 'event'

urlpatterns = [
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/<int:pk>/update/", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]
