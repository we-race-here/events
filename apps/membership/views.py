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

from ..usac.admin import usac_license_from_csv
from ..usac.forms import CsvImportForm
from .forms import OrganizationForm, OrganizationMemberJoinForm
from .member_utils import club_report
from .models import Organization, OrganizationMember

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

    def form_valid(self, form):
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


class OrganizationListView(ListView):
    model = Organization
    template_name = "org/organization_list.html"
    context_object_name = "organizations"
    paginate_by = 10
    ordering = ["name"]

    # Change this to the desired number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_choices"] = Organization.TYPE_CHOICES
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter only if OrganizationMember
        # user = self.request.user
        # if user.is_authenticated:
        #     queryset = queryset.filter(organizationmember__user=user)

        # Sorting
        sort_by = self.request.GET.get("sort", "")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        search_query = self.request.GET.get("search", "")
        type_filter = self.request.GET.get("type", "")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )

        if type_filter:
            queryset = queryset.filter(type=type_filter)

        return queryset


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
    """https://github.com/we-race-here/wrh-organization/blob/70623139387a97e83a96571dc2ab83db800ceac7/wrh_organization/apps/cycling_org/rest_api/views.py#L501"""

    template_name = "org/organization_admin.html"
    model = Organization
    context_object_name = "org"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        if self.request.POST.get("join_bc", None):
            # price = Price.objects.get(id=self.kwargs["pk"])
            # price_1N9pqlL1pkhMLFYAUvM0NqDS
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    customer_email="v@vdavis.net",
                    invoice_creation={"enabled": True},
                    payment_intent_data={
                        "metadata": {"club_dues": "2023_test"},
                    },
                    # metadata={
                    #     "club_dues": "2023",
                    # },
                    line_items=[
                        {
                            "price_data": {
                                "currency": "usd",
                                "unit_amount": 123,
                                "product_data": {
                                    "name": "2023 Club Dues",
                                    "description": "You club dues for 2023",
                                    # "images": ["https://example.com/t-shirt.png"],
                                },
                            },
                            "quantity": 1,
                        }
                    ],
                    # line_items=[
                    #     {
                    #         "price": "price_1N9pqlL1pkhMLFYAUvM0NqDS",
                    #         "quantity": 1,
                    #     },
                    # ],
                    mode="payment",
                    success_url="http://localhost:8000/org/10/",
                    cancel_url="http://localhost:8000/org/10/",
                )
            except Exception as e:
                return str(e)
            return redirect(checkout_session.url)

        # return self.render_to_response(context)


class BCAdminView(LoginRequiredMixin, TemplateView):
    template_name = "admin/bcadmin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST.get("usacdownload", None):
            form = CsvImportForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                csv_file = self.request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8").splitlines()
                context.update(usac_license_from_csv(decoded_file))
                return self.render_to_response(context)
        form = CsvImportForm()
        context.update({"form": form})
        return self.render_to_response(context)

    def get(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clubs"] = club_report()
        form = CsvImportForm()
        context.update({"form": form})
        return self.render_to_response(context)


"""
Alternative checkout setup
stripe.checkout.Session.create(
  success_url=success_url,
  cancel_url=cancel_url,
  payment_method_types=["card"],
  mode="payment",
  metadata={
    "foo": "FOO",
  },
  payment_intent_data={
    "metadata": {
      "bar": "BAR",
    }
  },
  line_items=[
    {
      "name": product_name,
      "quantity": quantity,
      "currency": currency,
      "amount": unit_price,
    },
  ]
)
"""
