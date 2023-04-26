from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Event
from .forms import EventForm

# Create
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_create.html"

# Read
class EventListView(ListView):
    model = Event
    template_name = "event/event_list.html"

class EventDetailView(DetailView):
    model = Event
    template_name = "event/event_detail.html"

# Update
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_update.html"

# Delete
class EventDeleteView(DeleteView):
    model = Event
    template_name = "event/event_delete.html"
    success_url = reverse_lazy("event_list")
