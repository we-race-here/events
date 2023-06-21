from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..membership.models import OrganizationMember
from .filters import EventFilter
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


class EventListView(ListView):
    model = Event
    template_name = "event/event_list.html"
    context_object_name = "events"
    paginate_by = 25
    ordering = ["end_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Champion Events
        context["champions"] = Event.objects.all().filter(Q(champion_event=True) & Q(end_date__gte=date.today()))
        #  Feature event
        context["featured"] = self.filter.qs.filter(featured_event=True)[:8]
        # Get page_obj from context
        context.update(
            {k: self.request.GET.get(k, None) for k in ["is_usac_permitted", "featured_event", "past_events"]}
        )
        page_obj = context.get("page_obj", None)
        if page_obj is not None:
            # We will show page numbers for 3 pages on each side of the current page
            start_page = max(page_obj.number - 3, 1)
            end_page = min(page_obj.number + 3, page_obj.paginator.num_pages)

            # Create list of page numbers
            page_range = list(range(start_page, end_page + 1))
            context["custom_page_range"] = page_range

        context["total_count"] = self.get_queryset().count()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if "past_events" not in self.request.GET:
            queryset = queryset.filter(end_date__gte=date.today())

        self.filter = EventFilter(self.request.GET, queryset=queryset)
        return self.filter.qs


# class EventListView(ListView):
#     model = Event
#     template_name = "event/event_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["events"] = Event.objects.all().order_by("start_date").filter(end_date__gte=date.today())
#         context["featured"] = context["events"].filter(featured_event=True)[:4]
#         return context
#
#     def get(self, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         queryset = Event.objects.all().order_by("start_date").filter(end_date__gte=date.today())
#         search_query = self.request.GET.get("search", "")
#         filter_usac = self.request.GET.get("filter_usac", "")
#         filter_featured = self.request.GET.get("filter_featured", "")
#         if any([search_query, filter_usac, filter_featured]):
#             if search_query:
#                 queryset = queryset.filter(
#                     Q(name__icontains=search_query)
#                     | Q(website__icontains=search_query)
#                     | Q(city__icontains=search_query)
#                     | Q(state__icontains=search_query)
#                 )
#             if filter_usac:
#                 queryset = queryset.filter(is_usac_permitted=True)
#             if filter_featured:
#                 queryset = queryset.filter(featured_event=True)
#             context["featured"] = None
#             context["events"] = queryset
#             return self.render_to_response(context)
#         else:
#             context["featured"] = queryset.filter(featured_event=True)[:4]
#             context["events"] = queryset
#             return self.render_to_response(context)


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

    def get_initial(self):
        women = [
            "Women 9-10",
            "Women 11-12",
            "Women 13-14",
            "Women 15-16",
            "Women 17-18",
            "Women 1-2",
            "Women 3",
            "Women 4",
            "Women 40+",
            "Women 50+",
            "Women 60+",
        ]
        men = [
            "Men 9-10",
            "Men 11-12",
            "Men 13-14",
            "Men 15-16",
            "Men 17-18",
            "Men 1-2",
            "Men 3",
            "Men 4",
            "Men 40+ 1-2-3",
            "Men 40+ 3",
            "Men 40+ 4",
            "Men 50+ 1-2-3",
            "Men 50+ 4",
            "Men 60+",
            "Men 70+",
        ]
        categories = women + men
        return {
            "categories": categories,
            "points_map": [35, 30, 27, 24, 22, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "point_system": "Relative",
            "organization": "Bicycle Colorado",
        }


class RaceSeriesDetailView(DetailView):
    model = RaceSeries
    context_object_name = "raceseries"
    template_name = "results/raceseries_detail.html"
    ordering = ["start_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Races"] = context["raceseries"].races.all()
        context["RaceResults"] = RaceResult.objects.filter(race__in=context["Races"])
        return context


def RaceResultsImportView(request, event_pk):
    context = {}
    event = get_object_or_404(Event, id=event_pk)  # GET method - render upload form
    raceseries = RaceSeries.objects.filter(events__id=event_pk)
    context["races"] = event.races.all()
    context["raceseries"] = raceseries
    context["event"] = event
    if request.method == "POST":
        form = RaceResultsImport(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["results_file"]
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            raceseries = form.cleaned_data["raceseries"]
            category_validation = form.cleaned_data["category_validation"]
            is_usac = form.cleaned_data["is_usac"]
            # form.cleaned_data["club_validation"]

            ir = ImportResults(file=decoded_file, is_usac=is_usac)
            ir.check_columns()
            ir.read_csv()
            ir.check_categories(category_validation)
            if ir.errors:
                # TODO: need a html page for this
                context.update({"errors": ir.errors})
                context.update({"warnings": ir.warnings})
                context.update({"form": form})
                print(context.keys())
                return render(request, "results/import_race_results.html", context=context)
            else:
                # TODO: Save results to database
                del form.cleaned_data["results_file"]
                fields_excluded = ["is_usac", "event", "raceseries", "category_validation"]
                # print(form.cleaned_data)
                update_form = {
                    field: value for field, value in form.cleaned_data.items() if field not in fields_excluded
                }
                update_form["event"] = event
                update_form["categories"] = list(ir.data_categories)
                r, c = Race.objects.update_or_create(
                    event=update_form["event"], name=update_form["name"], defaults=update_form
                )
                raceseries.races.add(r)
                [row.update(race=r) for row in ir.data]

                RaceResult.objects.bulk_create([RaceResult(**row) for row in ir.data])
                context.update({"warnings": ir.warnings})
                return render(request, "results/import_race_results.html", context=context)
        else:
            context.update({"errors": form.errors})
            context.update({"form": form})
            return render(request, "results/import_race_results.html", context=context)
    elif request.method == "GET":
        form = RaceResultsImport(initial={"event": event_pk, "raceseries": raceseries})
        context.update({"form": form})
        return render(request, "results/import_race_results.html", context)


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
