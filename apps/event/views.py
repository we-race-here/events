from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..membership.models import OrganizationMember
from .forms import EventForm
from .models import Event

# Read
event_edit_fields = {
    "PublicFields": ["name", "start_date", "end_date", "website", "city", "state", "country"],
    "UserFields": ["blurb", "description", "email", "registration_website", "is_usac_permitted", "permit_no", "tags"],
    "OrgAdminFields": ["featured_event", "publish_type", "panels"],
    "StaffFields": ["organization", "approved"],
}


class EventListView(ListView):
    model = Event
    template_name = "event/event_list.html"


class EventDetailView(DetailView):
    model = Event
    template_name = "event/event_detail.html"


# Create
class EventCreateView(CreateView):
    """ "
    Form fields
    ['name', 'featured_event', 'blurb', 'description', 'start_date', 'end_date', 'email', 'website',
     'registration_website',
     'permit_no', 'is_usac_permitted', 'city', 'state', 'country', 'tags', 'panels', 'organization', 'publish_type',
     'approved']"""

    # TODO: If user is_staff, approved is set to True
    # TODO: Org admins can only select their own organizations
    # TODO: is_staff can share with any org
    # TODO: Default Org is BC
    # TODO: add turnstile is not is_authenticaed user
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(event_edit_fields)
        context["IsOrgAdmin"] = OrganizationMember.objects.filter(user=self.request.user.id, is_admin=True)
        return context

    # TODO: send email to user and staff
    template_name = "event_form.html"
    success_url = reverse_lazy("event:event_list")


# Update
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(event_edit_fields)
        context["EventAdmin"] = OrganizationMember.objects.filter(
            Q(user=self.request.user.id) & Q(is_admin=True) & Q(organization=self.object.organization)
        )
        return context

    template_name = "event/event_form.html"
    success_url = reverse_lazy("event:event_list")


# Delete
class EventDeleteView(DeleteView):
    model = Event
    template_name = "event/event_delete.html"
    success_url = reverse_lazy("event_list")
