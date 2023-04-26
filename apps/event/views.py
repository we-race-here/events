from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event
from ..membership.models import OrganizationMember
from .forms import EventForm

event_edit_fields = {'PublicFields': ['name', 'start_date','end_date','website', 'city', 'state', 'country'],
                        'UserFields': ['blurb', 'description', 'email', 'registration_website', 'is_usac_permitted', 'permit_no', 'tags'],
                        'OrgAdminFields': ['featured_event', 'publish_type', 'panels'],
                        'StaffFields': ['organization', 'approved']}

class EventListView(ListView):
    model = Event
    template_name = 'event/event_list.html'

class EventCreateView(CreateView):
    """"
    Form fields
    ['name', 'featured_event', 'blurb', 'description', 'start_date', 'end_date', 'email', 'website',
     'registration_website',
     'permit_no', 'is_usac_permitted', 'city', 'state', 'country', 'tags', 'panels', 'organization', 'publish_type',
     'approved']"""
    model = Event
    form_class = EventForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(event_edit_fields)
        context['IsOrgAdmin'] = OrganizationMember.objects.filter(user=self.request.user.id, is_admin=True)
        return context
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:event_list')

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    # TODO: If user is_staff, approved is set to True
    # TODO: Org admins can only select their own organizations
    # TODO: is_staff can share with any org
    # TODO: Default Org is BC
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(event_edit_fields)
        context['IsOrgAdmin'] = OrganizationMember.objects.filter(Q(user=self.request.user.id) & Q(is_admin=True))
        return context
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event:event_list')
