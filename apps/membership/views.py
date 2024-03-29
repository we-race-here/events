# views.py
import csv
import datetime

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from events.users.permission_utils import StaffRequiredMixin
from events.utils.events_utils import sys_send_mail
from .forms import OrganizationForm, OrganizationMemberJoinForm
from .member_utils import club_report, get_club_payments
from .models import Organization, OrganizationMember
from ..store.stripe_utils import single_item_checkout

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


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

        # As we are saving org_type in form_valid - commenting out
        # if self.request.GET.get("org_type") == "Club":
        #     context["org_type"] = (Organization.TYPE_CLUB, "Club")
        # elif self.request.GET.get("org_type") == "Promoter":
        #     context["org_type"] = (Organization.TYPE_PROMOTER, "Promoter")

        return context

    def form_valid(self, form):
        # print("VALID")
        # print(form.cleaned_data)

        # Update ORG Type
        # If we need to show in frontend of selecting type. then we have to change the logic
        org_type = self.request.GET.get("org_type")
        if org_type == "Club":
            form.instance.type = Organization.TYPE_CLUB
        elif org_type == "Regional":
            form.instance.type = Organization.TYPE_REGIONAL
        elif org_type == "Advocacy, Volunteer":
            form.instance.type = Organization.TYPE_ADVOCACY_VOLUNTEER
        elif org_type == "Photographer":
            form.instance.type = Organization.TYPE_PHOTOGRAPHER
        elif org_type == "Promoter":
            form.instance.type = Organization.TYPE_PROMOTER

        organization = form.save(commit=False)
        organization.approved = True
        organization.save()

        # Create a new OrganizationMember instance with is_admin set to True
        organization_member = OrganizationMember(user=self.request.user, organization=organization, is_admin=True)
        organization_member.save()

         # Generate the full URL for the organization detail page
        organization_detail_url = self.request.build_absolute_uri(reverse('membership:organization_detail', args=[organization.pk]))

        # TODO: is it possible to get the Org id so that we can link to the org detail page from the email?
        # Use - organization
        html_message = render_to_string(
            "emails/new_org_email.html",
            {
                "TYPE": self.request.GET.get("org_type"),
                "NAME": form.cleaned_data["name"],
                "BYNAME": self.request.user.full_name,
                "ORGANIZATION_DETAIL_URL": organization_detail_url
            },
        )
        sys_send_mail(
            subject=f"\U0001F4C5 {form.cleaned_data['name']} event submitted for review",
            message=strip_tags(html_message),
            from_email="donotreply@bicyclecolorado.org",
            recipient_list=[self.request.user.email],
            recipient_system=settings.CALENDAR_EMAILS,
            html_message=html_message,
            fail_silently=False,
        )
        return redirect("membership:organization_detail", pk=organization.pk)


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = "org/organization_detail.html"
    context_object_name = "org"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["OrgAdmins"] = OrganizationMember.objects.filter(
            Q(user=self.request.user.id) & Q(is_admin=True) & Q(organization=self.object)
        )
        # Check if the user is authenticated before filtering
        if self.request.user.is_authenticated:
            context["is_member"] = OrganizationMember.objects.filter(
                user=self.request.user,
                organization=self.object
            ).exists()
        else:
            context["is_member"] = False
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
        # Check if the request.user is an admin in this organization
        is_request_user_admin = OrganizationMember.objects.filter(
            organization=self.object,
            user=self.request.user,
            is_admin=True
        ).exists()

        context['is_request_user_admin'] = is_request_user_admin
        context['current_user'] = self.request.user
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


class JoinClubView(LoginRequiredMixin, View):
    def get(self, request, pk):
        org = get_object_or_404(Organization, pk=pk)
        return render(request, 'org/join_club.html', {'org': org})

    def post(self, request, pk):
        org = get_object_or_404(Organization, pk=pk)
        accepted_waiver = request.POST.get('accept_waiver') == 'on'

        if accepted_waiver:
            OrganizationMember.objects.create(
                organization=org,
                user=request.user,
                is_admin=False,
                is_active=True,
                start_date=datetime.datetime.now()
            )
            messages.success(request, 'Successfully joined the club.')
            return redirect(reverse('membership:organization_detail', kwargs={'pk': org.pk}))

        messages.error(request, 'You must accept the waiver to join.')
        return render(request, 'join_club.html', {'org': org})


class LeaveClubView(LoginRequiredMixin, View):
    def post(self, request, pk):
        org = get_object_or_404(Organization, pk=pk)

        try:
            org_member = OrganizationMember.objects.get(
                organization=org,
                user=request.user
            )
            org_member.delete()

            messages.success(request, 'Successfully left the club.')
        except OrganizationMember.DoesNotExist:
            messages.error(request, 'You are not a member of this club.')

        return redirect(reverse('membership:organization_detail', kwargs={'pk': org.pk}))


class PromoteMemberView(LoginRequiredMixin, View):

    def get(self, request, pk, member_id, *args, **kwargs):
        try:
            # Validate that the organization exists and the user is an admin
            org = Organization.objects.get(pk=pk)
            if not OrganizationMember.objects.filter(user=request.user, organization=org, is_admin=True).exists():
                return JsonResponse({'status': 'Unauthorized'}, status=401)

            # Validate that the member exists within this organization
            member = OrganizationMember.objects.get(id=member_id, organization=org)
            member.is_admin = not member.is_admin  # Toggle the is_admin flag
            member.save()

            return JsonResponse({'status': 'success'})

        except Organization.DoesNotExist:
            return JsonResponse({'status': 'Organization does not exist'}, status=404)
        except OrganizationMember.DoesNotExist:
            return JsonResponse({'status': 'Member does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'An error occurred: ' + str(e)}, status=500)

class ExportCSV(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        # Find the organization and its members
        org = Organization.objects.get(pk=pk)
        members = OrganizationMember.objects.filter(organization=org)

        # Create the HttpResponse object with the appropriate headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{org.name}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Address'])  # Header

        for member in members:
            writer.writerow([member.user.full_name, member.user.email, member.user.phone, member.user.address1])

        return response
