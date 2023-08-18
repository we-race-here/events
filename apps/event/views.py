from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, FormView

from events.users.permission_utils import is_org_admin, StaffRequiredMixin
from events.utils.events_utils import sys_send_mail
from .forms import (
    RaceForm,
    RaceResultForm,
    RaceResultsImport,
    RaceSeriesForm,
    EventStaffForm,
    EventOrgAdminForm,
    EventAuthenticatedUserForm,
    EventCommunityForm,
)
from .models import Event, Race, RaceResult, RaceSeries
from .validators import ImportResults
from ..membership.models import OrganizationMember, Organization

User = get_user_model()


class EventListView(ListView):
    model = Event
    template_name = "event/event_list.html"
    context_object_name = "events"
    paginate_by = 25
    ordering = ["end_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Champion Events
        context["champions"] = Event.objects.all().filter(
            Q(champion_event=True) & Q(end_date__gte=date.today()) & Q(approved=True)
        )
        #  Feature event
        context["featured"] = Event.objects.all().filter(Q(featured_event=True) & Q(approved=True))[:8]
        context["filtered"] = bool(self.request.GET)

        # Get page_obj from context
        page_obj = context.get("page_obj", None)
        if page_obj is not None:
            # We will show page numbers for 3 pages on each side of the current page
            start_page = max(page_obj.number - 3, 1)
            end_page = min(page_obj.number + 3, page_obj.paginator.num_pages)

            # Create list of page numbers
            page_range = list(range(start_page, end_page + 1))
            context["custom_page_range"] = page_range

        context["total_count"] = self.get_queryset().count()
        withpage = self.request.GET.copy()
        withpage.pop("page", None)
        context["withpage"] = "&" + withpage.urlencode() if withpage else ""
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        if "past_events" not in self.request.GET:
            queryset = queryset.filter(Q(end_date__gte=date.today()) & Q(approved=True))
        else:
            queryset = queryset.filter(Q(start_date__lte=date.today()) & Q(approved=True))
        search_query = self.request.GET.get("search", "")
        filter_usac = self.request.GET.get("filter_usac", "")
        filter_featured = self.request.GET.get("filter_featured", "")
        if any([search_query, filter_usac, filter_featured]):
            if search_query:
                queryset = queryset & queryset.filter(
                    Q(name__icontains=search_query)
                    | Q(website__icontains=search_query)
                    | Q(city__icontains=search_query)
                    | Q(state__icontains=search_query)
                )
            if filter_usac:
                queryset = queryset & queryset.filter(is_usac_permitted=True)
            if filter_featured:
                queryset = queryset & queryset.filter(featured_event=True)
        return queryset


class EventsWaitingApproval(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/events_waiting_approval.html"
    context_object_name = "events"
    ordering = ["start_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(approved=False)

        search_term = self.request.GET.get('search_term')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        return queryset

    def post(self, request, *args, **kwargs):
        event_ids = request.POST.getlist('event_ids')
        if event_ids:
            Event.objects.filter(id__in=event_ids).update(approved=True)
        return redirect(reverse('event:events_waiting_approval'))  # Redirect back to the same page after approval

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


class EventCreateView(CreateView):
    model = Event
    template_name = "event/event_create.html"
    success_url = reverse_lazy("event:event_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            if self.request.user.is_staff:
                context["user_type"] = "EventStaffForm"
            elif is_org_admin(self.request.user):
                context["user_type"] = "EventOrgAdminForm"
            elif self.request.user.is_authenticated:
                context["user_type"] = "EventAuthenticatedUserForm"
        else:
            context["user_type"] = "EventCommunityForm"
        context["GOOGLE_MAP_API_TOKEN"] = settings.GOOGLE_MAP_API_TOKEN
        return context

    def get_form_class(self):
        if not self.request.user.is_anonymous:
            if self.request.user.is_staff:
                return EventStaffForm
            elif is_org_admin(self.request.user):
                return EventOrgAdminForm
            elif self.request.user.is_authenticated:
                return EventAuthenticatedUserForm
        else:
            return EventCommunityForm

    def get_form(self):
        form = super().get_form()
        if "organization" in form.fields:
            if self.request.user.is_staff:
                queryset = Organization.objects.all()
            else:
                queryset = Organization.objects.filter(Q(members__user=self.request.user) & Q(members__is_admin=True))
            form.fields["organization"].queryset = queryset
        return form

    # def form_invalid(self, form):
    #     print("invalide form")
    #     print(form.errors)
    #     return super().form_invalid(form)

    def form_valid(self, form):
        """add unicode for calendar to subject \U0001F4C5"""
        if not self.request.user.is_anonymous:
            user_email = self.request.user.email
            user_name = self.request.user.full_name
        else:
            user_email = form.cleaned_data["user_email"]
            user_name = form.cleaned_data["user_first"] + " " + form.cleaned_data["user_last"]

        html_message = render_to_string(
            "emails/new_event_created_email.html",
            {
                "NAME": user_name,
                "EMAIL": user_email,
                "EVENT_NAME": form.cleaned_data["name"],
            },
        )

        sys_send_mail(
            subject=f"\U0001F4C5 {form.cleaned_data['name']} event submitted for review",
            message="Thanks for submitting an event to Bicycle Colorado. We review each event manually and will let you "
            "know when it is approved.",
            from_email="donotreply@bicyclecolorado.org",
            recipient_list=[user_email],
            recipient_system=settings.CALENDAR_EMAILS,
            html_message=html_message,
            fail_silently=False,
        )
        return super().form_valid(form)


# Update
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "event/event_update.html"
    success_url = reverse_lazy("event:event_list")

    def get_form_class(self):
        if self.request.user.is_staff:
            return EventStaffForm
        elif is_org_admin(self.request.user):
            return EventOrgAdminForm
        else:
            return None

    def get_form(self):
        form = super().get_form()
        if "organization" in form.fields:
            if self.request.user.is_staff:
                queryset = Organization.objects.all()
            else:
                queryset = Organization.objects.filter(Q(members__user=self.request.user) & Q(members__is_admin=True))
            form.fields["organization"].queryset = queryset
        return form


# Delete
class EventDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
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
            if ir.errors:
                # TODO: need a html page for this
                context.update({"errors": ir.errors})
                context.update({"warnings": ir.warnings})
                context.update({"form": form})
                print(context.keys())
                return render(request, "results/import_race_results.html", context=context)
            else:
                ir.read_csv()
                if not ir.check_categories(category_validation):
                    # TODO: need a html page for this
                    context.update({"errors": ir.errors})
                    context.update({"warnings": ir.warnings})
                    context.update({"form": form})
                    print(context.keys())
                    return render(request, "results/import_race_results.html", context=context)
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
