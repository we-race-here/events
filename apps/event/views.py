from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from ..membership.models import OrganizationMember
from .forms import EventForm, RaceForm, RaceResultForm, RaceResultsImport, RaceSeriesForm
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


class EventListView(TemplateView):
    template_name = "event/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all().order_by("start_date").filter(end_date__gte=date.today())
        context["featured"] = context["events"].filter(featured_event=True)[:4]
        return context

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        queryset = Event.objects.all().order_by("start_date").filter(end_date__gte=date.today())
        search_query = self.request.GET.get("search", "")
        filter_usac = self.request.GET.get("filter_usac", "")
        filter_featured = self.request.GET.get("filter_featured", "")
        if any([search_query, filter_usac, filter_featured]):
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query)
                    | Q(website__icontains=search_query)
                    | Q(city__icontains=search_query)
                    | Q(state__icontains=search_query)
                )
            if filter_usac:
                queryset = queryset.filter(is_usac_permitted=True)
            if filter_featured:
                queryset = queryset.filter(featured_event=True)
            context["featured"] = None
            context["events"] = queryset
            return self.render_to_response(context)
        else:
            context["featured"] = queryset.filter(featured_event=True)[:4]
            context["events"] = queryset
            return self.render_to_response(context)


class EventResultListView(ListView):
    model = Event
    template_name = "results/events_results_list.html"
    context_object_name = "events"

    # paginate_by = 10  # Change this to the desired number of items per page
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["RaceSeries"] = RaceSeries.objects.all()

        return context

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
        context["GOOGLE_MAP_API_TOKEN"] = settings.GOOGLE_MAP_API_TOKEN
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


class RaceSeriesUpdateView(LoginRequiredMixin, UpdateView):
    model = RaceSeries
    form_class = RaceSeriesForm
    template_name = "results/raceseries_form.html"
    success_url = reverse_lazy("event:events_results_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RaceSeriesCreateView(LoginRequiredMixin, CreateView):
    model = RaceSeries
    form_class = RaceSeriesForm
    template_name = "results/raceseries_form.html"
    success_url = reverse_lazy("event:events_results_list")


class RaceSeriesDetailView(DetailView):
    model = RaceSeries
    context_object_name = "raceseries"
    template_name = "results/raceseries_detail.html"
    ordering = ["start_date"]


def RaceResultsImportView(request, event_pk):
    context = {}
    event = get_object_or_404(Event, id=event_pk)  # GET method - render upload form
    raceseries = RaceSeries.objects.filter(events__id=event_pk)
    context["races"] = event.races.all()
    context["raceseries"] = raceseries
    context["event"] = event
    print(context)
    if request.method == "POST":
        form = RaceResultsImport(request.POST, request.FILES)
        if form.is_valid():
            context = {}
            csv_file = request.FILES["results_file"]
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            raceseries = form.cleaned_data["raceseries"]
            category_validation = form.cleaned_data["category_validation"]
            form.cleaned_data["category_raceseries"]
            license_validation = form.cleaned_data["license_validation"]
            form.cleaned_data["club_validation"]

            ir = ImportResults(
                decoded_file,
                category_validation,
                license_validation,
            )
            ir.read_csv()
            ir.pii_check()
            ir.check_columns()
            if ir.errors:
                # TODO: need a html page for this
                context.update({"errors": ir.errors})
                return render(request, "results/import_race_results.html", context=context)

            else:
                # TODO: Save results to database
                # del form.cleaned_data["results_file"]
                # Race.objects.create(**form.cleaned_data)
                # TODO, save file data to RaceResults
                return HttpResponse("Results imported successfully")
        else:
            return HttpResponse(f"Form is not valid: {form.errors}")
    elif request.method == "GET":
        print(context)
        form = RaceResultsImport(initial={"event": event_pk, "raceseries": raceseries})
        return render(request, "results/import_race_results.html", {"context": context, "form": form})


class RaceCreateView(LoginRequiredMixin, CreateView):
    model = Race
    form_class = RaceForm
    context_object_name = "race"
    template_name = "results/race_create.html"


class RaceResultCreateView(LoginRequiredMixin, CreateView):
    model = RaceResult
    form_class = RaceResultForm
    context_object_name = "raceresult"
    template_name = "results/raceresult_create.html"
