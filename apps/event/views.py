from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm

class EventListView(ListView):
    model = Event
    template_name = 'event/event_list.html'

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:event_list')

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event:event_list')
