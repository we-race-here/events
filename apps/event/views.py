from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..membership.models import OrganizationMember
from .forms import EventForm, RaceSeriesForm, UploadRaceResults
from .models import Event, Race, RaceResult, RaceSeries
from .validators import ImportResults

User = get_user_model()

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
    context_object_name = "events"

    # paginate_by = 10  # Change this to the desired number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Sorting
        sort_by = self.request.GET.get("sort", "")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )
        return queryset


class EventResultListView(ListView):
    model = Event
    template_name = "results/events_results_list.html"
    context_object_name = "events"

    # paginate_by = 10  # Change this to the desired number of items per page

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     return context
    #
    def get_queryset(self):
        queryset = Event.objects.filter(
            Q(start_date__lte=date.today()) & Q(Exists(Race.objects.filter(event=OuterRef("pk"))))
        ).order_by("-start_date")
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )
        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = "event/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["EventAdmin"] = OrganizationMember.objects.filter(
            Q(user=self.request.user.id) & Q(is_admin=True) & Q(organization=self.object.organization)
        )
        context["Races"] = Race.objects.filter(event=context["object"])
        context["RaceResults"] = RaceResult.objects.filter(race__in=context["Races"])
        return context


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
    template_name = "event/event_create.html"
    success_url = reverse_lazy("event:event_list")


# Update
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_update.html"
    success_url = reverse_lazy("event:event_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(event_edit_fields)
        context["EventAdmin"] = OrganizationMember.objects.filter(
            Q(user=self.request.user.id) & Q(is_admin=True) & Q(organization=self.object.organization)
        )
        return context


# Delete
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "event/event_delete.html"
    success_url = reverse_lazy("event_list")
    # TODO: Only is_staff should be able to delete an event


class RaceSeriesCreateView(LoginRequiredMixin, CreateView):
    model = RaceSeries
    form_class = RaceSeriesForm
    template_name = "results/raceseries_form.html"
    success_url = reverse_lazy("raceseries_list")


def ImportRaceResults(request, event_pk):
    if request.method == "POST":
        form = UploadRaceResults(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["results_file"]
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            ir = ImportResults(decoded_file)
            ir.read_csv()
            ir.pii_check()
            ir.check_columns()
            if ir.errors:
                # TODO: need a html page for this
                return HttpResponse(f"Please correct there errors: {ir.errors}")
            else:
                # TODO: Save results to database
                del form.cleaned_data["results_file"]
                Race.objects.create(**form.cleaned_data)
                # TODO, save file data to RaceResults
                return HttpResponse("Results imported successfully")
        else:
            return HttpResponse(f"Form is not valid: {form.errors}")
    elif request.method == "GET":
        get_object_or_404(Event, id=event_pk)  # GET method - render upload form
        form = UploadRaceResults(initial={"event": event_pk})
        return render(request, "results/import_race_results.html", {"form": form})
