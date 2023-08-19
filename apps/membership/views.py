# views.py

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from events.users.permission_utils import StaffRequiredMixin
from .forms import OrganizationForm, OrganizationMemberJoinForm
from .member_utils import club_report, get_club_payments
from .models import Organization, OrganizationMember
from ..store.stripe_utils import single_item_checkout

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsOrgAdminMixin(UserPassesTestMixin):
    # TODO: fix this.
    def test_func(self):
        OrganizationMember.objects.get(
            Q(user=self.request.user) & (Q(is_admin=True) | Q(organization__id=self.request))
        )
        return self.request.user.is_org_admin


class CreateOrganizationView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org/create_organization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("org_type") == "Club":
            context["org_type"] = (Organization.TYPE_CLUB, "Club")
        elif self.request.GET.get("org_type") == "Promoter":
            context["org_type"] = ((Organization.TYPE_PROMOTER, "Club"),)
        return context

    def form_valid(self, form):
        print("VALID")
        print(form.cleaned_data)
        organization = form.save(commit=False)
        organization.approved = self.request.user.is_staff
        organization.save()

        # Create a new OrganizationMember instance with is_admin set to True
        organization_member = OrganizationMember(user=self.request.user, organization=organization, is_admin=True)
        organization_member.save()

        # TODO: is it possible to get the Org id so that we can link to the org detail page from the email?
        # Use - organization
        html_message = render_to_string(
            "org/new_org_email.html",
            {
                "TYPE": form.cleaned_data["type"],
                "NAME": form.cleaned_data["name"],
                "BYNAME": self.request.user.full_name,
            },
        )
        plain_message = strip_tags(html_message)
        # This email is to the submitter
        send_mail(
            f"New {form.cleaned_data['type']} named: {form.cleaned_data['name']} is waiting approval",
            plain_message,
            "donotreply@bicyclecolorado.org",
            [self.request.user.email],
            html_message=html_message,
        )
        # This email is to the staff
        # [user.email for user in User.objects.filter(is_staff=True)]
        send_mail(
            f"New {form.cleaned_data['type']} named: {form.cleaned_data['name']} is waiting approval",
            plain_message,
            "donotreply@bicyclecolorado.org",
            ["developer@bicyclecolorado.org"],
            html_message=html_message,
        )
        return redirect("membership:organizations")


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = "org/organization_detail.html"
    context_object_name = "org"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["OrgAdmins"] = OrganizationMember.objects.filter(
            Q(user=self.request.user.id) & Q(is_admin=True) & Q(organization=self.object)
        )
        return context


class UpdateOrganizationView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org/update_organization.html"

    def get_success_url(self):
        return reverse("membership:organizations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteOrganizationView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    model = Organization
    template_name = "org/delete_organization.html"
    success_url = reverse_lazy("organizations")


class ClubListView(ListView):
    model = Organization
    template_name = "org/club_list.html"
    context_object_name = "organizations"
    paginate_by = 10
    ordering = ["name"]

    # Change this to the desired number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_choices"] = (
            (Organization.TYPE_CLUB, "Club"),
            (Organization.TYPE_ADVOCACY_VOLUNTEER, "Advocacy, Volunteer"),
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        base_queryset = queryset.filter(type__in=[Organization.TYPE_CLUB, Organization.TYPE_ADVOCACY_VOLUNTEER])
        # Filter only if OrganizationMember
        # user = self.request.user
        # if user.is_authenticated:
        #     queryset = queryset.filter(organizationmember__user=user)

        # Sorting
        # sort_by = self.request.GET.get("sort", "")
        # if sort_by:
        #     queryset = queryset.order_by(sort_by)
        search_query = self.request.GET.get("search", "")
        type_filter = self.request.GET.get("type", "")

        if search_query:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )

        if type_filter:
            base_queryset = base_queryset.filter(type=type_filter)

        return base_queryset


class PromoterListView(ListView):
    model = Organization
    template_name = "org/promoter_list.html"
    context_object_name = "promoters"
    paginate_by = 10
    ordering = ["name"]

    # Change this to the desired number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        base_queryset = queryset.filter(type=Organization.TYPE_PROMOTER)

        # Filter only if OrganizationMember
        # user = self.request.user
        # if user.is_authenticated:
        #     queryset = queryset.filter(organizationmember__user=user)

        search_query = self.request.GET.get("search", "")

        if search_query:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )

        return base_queryset


class JoinOrganizationView(FormView):
    template_name = "org/join_organization.html"
    form_class = OrganizationMemberJoinForm
    success_url = reverse_lazy("membership:organizations")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        organization_id = self.kwargs.get("organization_id")
        if organization_id:
            kwargs["organization"] = Organization.objects.get(pk=organization_id)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class OrganizationAdmin(LoginRequiredMixin, DetailView):
    template_name = "org/organization_admin.html"
    model = Organization
    context_object_name = "org"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = stripe.Product.retrieve("prod_NvhFVL6FC3AdKr")
        context["price"] = context["product"]["default_price"]
        context["club_payments"] = get_club_payments(self.object)
        return context

    def post(self, *args, **kwargs):
        {"org": self.get_object()}
        if self.request.POST.get("single_product", None):
            checkout_session = single_item_checkout(self.request, self.get_object())
            return redirect(checkout_session.url)


class ClubAdmin(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin/club_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clubs"] = club_report()

        return context

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
